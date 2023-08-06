#include <Windows.h>
#include <Python.h>

#define XBOX_DPAD_UP          0x0001
#define XBOX_DPAD_DOWN        0x0002
#define XBOX_DPAD_LEFT        0x0004
#define XBOX_DPAD_RIGHT       0x0008
#define XBOX_START            0x0010
#define XBOX_BACK             0x0020
#define XBOX_LEFT_THUMB       0x0040
#define XBOX_RIGHT_THUMB      0x0080
#define XBOX_LEFT_SHOULDER    0x0100
#define XBOX_RIGHT_SHOULDER   0x0200
#define XBOX_A                0x1000
#define XBOX_B                0x2000
#define XBOX_X                0x4000
#define XBOX_Y                0x8000

struct XINPUT_GAMEPAD {
	WORD Buttons;
	BYTE LT;
	BYTE RT;
	SHORT LX;
	SHORT LY;
	SHORT RX;
	SHORT RY;
};

struct XINPUT_STATE {
	DWORD ID;
	XINPUT_GAMEPAD Gamepad;
};

struct XINPUT_VIBRATION {
	WORD LMS;
	WORD RMS;
};

struct XINPUT_CALIBRATION {
	double LX;
	double LY;
	double RX;
	double RY;
};

DWORD WINAPI XInputGetStateDummy(DWORD user, XINPUT_STATE * value);
DWORD WINAPI XInputSetStateDummy(DWORD user, XINPUT_VIBRATION * value);
void WINAPI XInputEnableDummy(BOOL enable);

typedef decltype(XInputGetStateDummy) * XInputGetStateProc;
typedef decltype(XInputSetStateDummy) * XInputSetStateProc;
typedef decltype(XInputEnableDummy) * XInputEnableProc;

XInputGetStateProc XInputGetState;
XInputSetStateProc XInputSetState;
XInputEnableProc XInputEnable;

XINPUT_CALIBRATION Calibration[4];

typedef double (* NiceProc) (const double & x);

double nice0(const double & x) {
	return x;
}

double nice1(const double & x) {
	return (double)((int)(x * 1000.0) / 1000.0);
}

double nice2(const double & x) {
	return (double)((int)(x * 100.0) / 100.0);
}

double nice3(const double & x) {
	return (double)((int)(x * 10.0) / 10.0);
}

NiceProc nice = nice0;

double clamped(const double & x, const double & a, const double & b) {
	if (x < a) {
		return a;
	} else if (x < b) {
		return x;
	} else {
		return b;
	}
}

double SmoothStickValue(const double & val, const double & base) {
	double result = val - base;

	if (result >= 0.0) {
		return nice(clamped(result / (32767.0 - base), -1.0, 1.0));
	} else {
		return nice(clamped(result / (32768.0 + base), -1.0, 1.0));
	}
}

PyObject * RawInput(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"user", 0};

	int user = 0;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|$I:Input", (char **)kwlist, &user)) {
		return 0;
	}

	PyObject * result = PyDict_New();

	XINPUT_STATE state = {};
	XInputGetState(user, &state);

	PyDict_SetItemString(result, "ID", PyLong_FromLong(state.ID));
	PyDict_SetItemString(result, "Buttons", PyLong_FromLong(state.Gamepad.Buttons));
	PyDict_SetItemString(result, "LT", PyLong_FromLong(state.Gamepad.LT));
	PyDict_SetItemString(result, "RT", PyLong_FromLong(state.Gamepad.RT));
	PyDict_SetItemString(result, "LX", PyLong_FromLong(state.Gamepad.LX));
	PyDict_SetItemString(result, "LY", PyLong_FromLong(state.Gamepad.LY));
	PyDict_SetItemString(result, "RX", PyLong_FromLong(state.Gamepad.RX));
	PyDict_SetItemString(result, "RY", PyLong_FromLong(state.Gamepad.RY));

	return result;
}

PyObject * RawVibrate(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"left", "right", "user", 0};

	int left;
	int right;
	int user = 0;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "II|$I:Vibrate", (char **)kwlist, &left, &right, &user)) {
		return 0;
	}

	XINPUT_VIBRATION state = {(WORD)left, (WORD)right};
	XInputSetState(user, &state);

	Py_RETURN_NONE;
}

PyObject * Input(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"user", 0};

	int user = 0;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|$I:Input", (char **)kwlist, &user)) {
		return 0;
	}

	if (user < 0 || user >= 4) {
		return 0;
	}

	PyObject * result = PyDict_New();

	XINPUT_STATE state = {};
	XInputGetState(user, &state);

	PyDict_SetItemString(result, "Buttons", PyLong_FromLong(state.Gamepad.Buttons));
	PyDict_SetItemString(result, "LT", PyFloat_FromDouble(nice(state.Gamepad.LT / 255.0)));
	PyDict_SetItemString(result, "RT", PyFloat_FromDouble(nice(state.Gamepad.RT / 255.0)));

	PyDict_SetItemString(result, "LX", PyFloat_FromDouble(SmoothStickValue(state.Gamepad.LX, Calibration[user].LX)));
	PyDict_SetItemString(result, "LY", PyFloat_FromDouble(SmoothStickValue(state.Gamepad.LY, Calibration[user].LY)));
	PyDict_SetItemString(result, "RX", PyFloat_FromDouble(SmoothStickValue(state.Gamepad.RX, Calibration[user].RX)));
	PyDict_SetItemString(result, "RY", PyFloat_FromDouble(SmoothStickValue(state.Gamepad.RY, Calibration[user].RY)));

	return result;
}

PyObject * Vibrate(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"left", "right", "user", 0};

	double left;
	double right;
	int user = 0;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd|$I:Vibrate", (char **)kwlist, &left, &right, &user)) {
		return 0;
	}

	if (user < 0 || user >= 4) {
		return 0;
	}

	XINPUT_VIBRATION state = {(WORD)(clamped(left, 0.0, 1.0) * 65535.0 + 0.5), (WORD)(clamped(right, 0.0, 1.0) * 65535.0 + 0.5)};
	XInputSetState(user, &state);

	Py_RETURN_NONE;
}

PyObject * Calibrate(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"user", 0};

	int user = 0;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|$I:Input", (char **)kwlist, &user)) {
		return 0;
	}

	if (user < 0 || user >= 4) {
		return 0;
	}

	XINPUT_STATE state = {};
	XInputGetState(user, &state);
	Calibration[user] = {
		(double)state.Gamepad.LX,
		(double)state.Gamepad.LY,
		(double)state.Gamepad.RX,
		(double)state.Gamepad.RY,
	};

	Py_RETURN_NONE;
}

PyObject * Filter(PyObject * self, PyObject * args, PyObject * kwargs) {
	static const char * kwlist[] = {"filter", 0};

	int filter = 0;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "I:Filter", (char **)kwlist, &filter)) {
		return 0;
	}

	switch (filter) {
		case 0:
			nice = nice0;
			break;

		case 1:
			nice = nice1;
			break;

		case 2:
			nice = nice2;
			break;

		case 3:
			nice = nice3;
			break;

		default:
			return 0;
	}

	Py_RETURN_NONE;
}

PyMethodDef methods[] = {
	{"Calibrate", (PyCFunction)Calibrate, METH_VARARGS | METH_KEYWORDS, 0},
	{"Filter", (PyCFunction)Filter, METH_VARARGS | METH_KEYWORDS, 0},
	{"RawInput", (PyCFunction)RawInput, METH_VARARGS | METH_KEYWORDS, 0},
	{"RawVibrate", (PyCFunction)RawVibrate, METH_VARARGS | METH_KEYWORDS, 0},
	{"Input", (PyCFunction)Input, METH_VARARGS | METH_KEYWORDS, 0},
	{"Vibrate", (PyCFunction)Vibrate, METH_VARARGS | METH_KEYWORDS, 0},
	{0},
};

PyModuleDef moduledef = {PyModuleDef_HEAD_INIT, "XboxController", 0, -1, methods, 0, 0, 0, 0};

extern "C" PyObject * PyInit_XboxController() {
	HMODULE xinput = LoadLibrary("xinput1_3.dll");

	if (!xinput) {
		return 0;
	}

	XInputGetState = (XInputGetStateProc)GetProcAddress(xinput, "XInputGetState");

	if (!XInputGetState) {
		return 0;
	}

	XInputSetState = (XInputSetStateProc)GetProcAddress(xinput, "XInputSetState");

	if (!XInputSetState) {
		return 0;
	}

	XInputEnable = (XInputEnableProc)GetProcAddress(xinput, "XInputEnable");

	if (!XInputEnable) {
		return 0;
	}

	PyObject * module = PyModule_Create(&moduledef);

	XInputEnable(true);
	
	for (int user = 0; user < 4; ++user) {
		XINPUT_STATE state = {};
		XInputGetState(user, &state);
		Calibration[user] = {
			(double)state.Gamepad.LX,
			(double)state.Gamepad.LY,
			(double)state.Gamepad.RX,
			(double)state.Gamepad.RY,
		};
	}

	if (module) {
		PyModule_AddIntConstant(module, "UP", 0x0001);
		PyModule_AddIntConstant(module, "DOWN", 0x0002);
		PyModule_AddIntConstant(module, "LEFT", 0x0004);
		PyModule_AddIntConstant(module, "RIGHT", 0x0008);
		PyModule_AddIntConstant(module, "START", 0x0010);
		PyModule_AddIntConstant(module, "BACK", 0x0020);
		PyModule_AddIntConstant(module, "LT", 0x0040);
		PyModule_AddIntConstant(module, "RT", 0x0080);
		PyModule_AddIntConstant(module, "LB", 0x0100);
		PyModule_AddIntConstant(module, "RB", 0x0200);
		PyModule_AddIntConstant(module, "A", 0x1000);
		PyModule_AddIntConstant(module, "B", 0x2000);
		PyModule_AddIntConstant(module, "X", 0x4000);
		PyModule_AddIntConstant(module, "Y", 0x8000);
	}

	return module;
}
