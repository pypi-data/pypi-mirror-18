# Generated definitions file
from zgoubi.core import zgoubi_element

class BEND(zgoubi_element):
	_class_name='BEND'
	_zgoubi_name='BEND'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IL']=0
		self._types['IL']='I'
		self._params['XL']=0
		self._types['XL']='E'
		self._params['Sk']=0
		self._types['Sk']='E'
		self._params['B1']=0
		self._types['B1']='E'
		self._params['X_E']=0
		self._types['X_E']='E'
		self._params['LAM_E']=0
		self._types['LAM_E']='E'
		self._params['W_E']=0
		self._types['W_E']='E'
		self._params['N']=0
		self._types['N']='I'
		self._params['C_0']=0
		self._types['C_0']='E'
		self._params['C_1']=0
		self._types['C_1']='E'
		self._params['C_2']=0
		self._types['C_2']='E'
		self._params['C_3']=0
		self._types['C_3']='E'
		self._params['C_4']=0
		self._types['C_4']='E'
		self._params['C_5']=0
		self._types['C_5']='E'
		self._params['X_S']=0
		self._types['X_S']='E'
		self._params['LAM_S']=0
		self._types['LAM_S']='E'
		self._params['W_S']=0
		self._types['W_S']='E'
		self._params['NS']=0
		self._types['NS']='I'
		self._params['CS_0']=0
		self._types['CS_0']='E'
		self._params['CS_1']=0
		self._types['CS_1']='E'
		self._params['CS_2']=0
		self._types['CS_2']='E'
		self._params['CS_3']=0
		self._types['CS_3']='E'
		self._params['CS_4']=0
		self._types['CS_4']='E'
		self._params['CS_5']=0
		self._types['CS_5']='E'
		self._params['XPAS']=0
		self._types['XPAS']='X'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['XCE']=0
		self._types['XCE']='E'
		self._params['YCE']=0
		self._types['YCE']='E'
		self._params['ALE']=0
		self._types['ALE']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'BEND' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IL']) +nl 
		out +=  E(self._params['XL']) + ' ' + E(self._params['Sk']) + ' ' + E(self._params['B1']) +nl 
		out +=  E(self._params['X_E']) + ' ' + E(self._params['LAM_E']) + ' ' + E(self._params['W_E']) +nl 
		out +=  I(self._params['N']) + ' ' + E(self._params['C_0']) + ' ' + E(self._params['C_1']) + ' ' + E(self._params['C_2']) + ' ' + E(self._params['C_3']) + ' ' + E(self._params['C_4']) + ' ' + E(self._params['C_5']) +nl 
		out +=  E(self._params['X_S']) + ' ' + E(self._params['LAM_S']) + ' ' + E(self._params['W_S']) +nl 
		out +=  I(self._params['NS']) + ' ' + E(self._params['CS_0']) + ' ' + E(self._params['CS_1']) + ' ' + E(self._params['CS_2']) + ' ' + E(self._params['CS_3']) + ' ' + E(self._params['CS_4']) + ' ' + E(self._params['CS_5']) +nl 
		out +=  X(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) + ' ' + E(self._params['XCE']) + ' ' + E(self._params['YCE']) + ' ' + E(self._params['ALE']) +nl 
		return out

class CAVITE(zgoubi_element):
	_class_name='CAVITE'
	_zgoubi_name='CAVITE'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IOPT']=0
		self._types['IOPT']='E'
		self._params['X']=0
		self._types['X']='E'
		self._params['X']=0
		self._types['X']='E'
		self._params['L']=0
		self._types['L']='E'
		self._params['h']=0
		self._types['h']='E'
		self._params['V']=0
		self._types['V']='E'
		self._params['X']=0
		self._types['X']='E'
		self._params['L']=0
		self._types['L']='E'
		self._params['h']=0
		self._types['h']='E'
		self._params['V']=0
		self._types['V']='E'
		self._params['sig_s']=0
		self._types['sig_s']='E'
		self._params['X']=0
		self._types['X']='E'
		self._params['X']=0
		self._types['X']='E'
		self._params['V']=0
		self._types['V']='E'
		self._params['sig_s']=0
		self._types['sig_s']='E'
		self._params['L']=0
		self._types['L']='E'
		self._params['h']=0
		self._types['h']='E'
		self._params['V']=0
		self._types['V']='E'
		self._params['sig_s']=0
		self._types['sig_s']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'CAVITE' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  E(self._params['IOPT']) +nl 
		if self._params['IOPT'] == 0 : out +=  E(self._params['X']) + ' ' + E(self._params['X']) +nl 
		if self._params['IOPT'] == 1 : out +=  E(self._params['L']) + ' ' + E(self._params['h']) +nl 
		if self._params['IOPT'] == 1 : out +=  E(self._params['V']) + ' ' + E(self._params['X']) +nl 
		if self._params['IOPT'] == 2 : out +=  E(self._params['L']) + ' ' + E(self._params['h']) +nl 
		if self._params['IOPT'] == 2 : out +=  E(self._params['V']) + ' ' + E(self._params['sig_s']) +nl 
		if self._params['IOPT'] == 3 : out +=  E(self._params['X']) + ' ' + E(self._params['X']) +nl 
		if self._params['IOPT'] == 3 : out +=  E(self._params['V']) + ' ' + E(self._params['sig_s']) +nl 
		if self._params['IOPT'] == 7 : out +=  E(self._params['L']) + ' ' + E(self._params['h']) +nl 
		if self._params['IOPT'] == 7 : out +=  E(self._params['V']) + ' ' + E(self._params['sig_s']) +nl 
		return out

class CHAMBR(zgoubi_element):
	_class_name='CHAMBR'
	_zgoubi_name='CHAMBR'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IA']=0
		self._types['IA']='I'
		self._params['IFORM']=0
		self._types['IFORM']='I'
		self._params['YL']=0
		self._types['YL']='E'
		self._params['ZL']=0
		self._types['ZL']='E'
		self._params['YC']=0
		self._types['YC']='E'
		self._params['ZC']=0
		self._types['ZC']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'CHAMBR' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IA']) +nl 
		out +=  I(self._params['IFORM']) + ' ' + E(self._params['YL']) + ' ' + E(self._params['ZL']) + ' ' + E(self._params['YC']) + ' ' + E(self._params['ZC']) +nl 
		return out

class CHANGREF(zgoubi_element):
	_class_name='CHANGREF'
	_zgoubi_name='CHANGREF'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['XCE']=0
		self._types['XCE']='E'
		self._params['YCE']=0
		self._types['YCE']='E'
		self._params['ALE']=0
		self._types['ALE']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'CHANGREF' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  E(self._params['XCE']) + ' ' + E(self._params['YCE']) + ' ' + E(self._params['ALE']) +nl 
		return out

class DIPOLES(zgoubi_element):
	_class_name='DIPOLES'
	_zgoubi_name='DIPOLES'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IL']=0
		self._types['IL']='I'
		self._params['N']=0
		self._types['N']='I'
		self._params['AT']=0
		self._types['AT']='E'
		self._params['RM']=0
		self._types['RM']='E'
		self._types['ACN']='E'
		self._types['DELTA_RM']='E'
		self._types['B_0']='E'
		self._types['IND']='I'
		self._types['BCOEF1']='E'
		self._types['BCOEF2']='E'
		self._types['BCOEF3']='E'
		self._types['BCOEF4']='E'
		self._types['BCOEF5']='E'
		self._types['BCOEF6']='E'
		self._types['BCOEF7']='E'
		self._types['BCOEF8']='E'
		self._types['BCOEF9']='E'
		self._types['BCOEF10']='E'
		self._types['G0_E']='E'
		self._types['KAPPA_E']='E'
		self._types['NCE']='I'
		self._types['CE_0']='E'
		self._types['CE_1']='E'
		self._types['CE_2']='E'
		self._types['CE_3']='E'
		self._types['CE_4']='E'
		self._types['CE_5']='E'
		self._types['SHIFT_E']='E'
		self._types['OMEGA_E']='E'
		self._types['THETA_E']='E'
		self._types['R1_E']='E'
		self._types['U1_E']='E'
		self._types['U2_E']='E'
		self._types['R2_E']='E'
		self._types['G0_S']='E'
		self._types['KAPPA_S']='E'
		self._types['NCS']='I'
		self._types['CS_0']='E'
		self._types['CS_1']='E'
		self._types['CS_2']='E'
		self._types['CS_3']='E'
		self._types['CS_4']='E'
		self._types['CS_5']='E'
		self._types['SHIFT_S']='E'
		self._types['OMEGA_S']='E'
		self._types['THETA_S']='E'
		self._types['R1_S']='E'
		self._types['U1_S']='E'
		self._types['U2_S']='E'
		self._types['R2_S']='E'
		self._types['G0_L']='E'
		self._types['KAPPA_L']='E'
		self._types['NCL']='I'
		self._types['CL_0']='E'
		self._types['CL_1']='E'
		self._types['CL_2']='E'
		self._types['CL_3']='E'
		self._types['CL_4']='E'
		self._types['CL_5']='E'
		self._types['SHIFT_L']='E'
		self._types['OMEGA_L']='E'
		self._types['THETA_L']='E'
		self._types['R1_L']='E'
		self._types['U1_L']='E'
		self._types['U2_L']='E'
		self._types['R2_L']='E'
		self._types['R3']='E'
		self._params['KIRD']=0
		self._types['KIRD']='E'
		self._params['RESOL']=0
		self._types['RESOL']='I'
		self._params['XPAS']=0
		self._types['XPAS']='E'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['RE']=0
		self._types['RE']='E'
		self._params['TE']=0
		self._types['TE']='E'
		self._params['RS']=0
		self._types['RS']='E'
		self._params['TS']=0
		self._types['TS']='E'
		self.set(settings)
		self._looped_data = []
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'DIPOLES' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IL']) +nl 
		out +=  I(self._params['N']) + ' ' + E(self._params['AT']) + ' ' + E(self._params['RM']) +nl 
		for part in self._looped_data:
			out +=  E(part['ACN']) + ' ' + E(part['DELTA_RM']) + ' ' + E(part['B_0']) + ' ' + I(part['IND']) + ' ' + E(part['BCOEF1']) + ' ' + E(part['BCOEF2']) + ' ' + E(part['BCOEF3']) + ' ' + E(part['BCOEF4']) + ' ' + E(part['BCOEF5']) + ' ' + E(part['BCOEF6']) + ' ' + E(part['BCOEF7']) + ' ' + E(part['BCOEF8']) + ' ' + E(part['BCOEF9']) + ' ' + E(part['BCOEF10']) +nl 
			out +=  E(part['G0_E']) + ' ' + E(part['KAPPA_E']) +nl 
			out +=  I(part['NCE']) + ' ' + E(part['CE_0']) + ' ' + E(part['CE_1']) + ' ' + E(part['CE_2']) + ' ' + E(part['CE_3']) + ' ' + E(part['CE_4']) + ' ' + E(part['CE_5']) + ' ' + E(part['SHIFT_E']) +nl 
			out +=  E(part['OMEGA_E']) + ' ' + E(part['THETA_E']) + ' ' + E(part['R1_E']) + ' ' + E(part['U1_E']) + ' ' + E(part['U2_E']) + ' ' + E(part['R2_E']) +nl 
			out +=  E(part['G0_S']) + ' ' + E(part['KAPPA_S']) +nl 
			out +=  I(part['NCS']) + ' ' + E(part['CS_0']) + ' ' + E(part['CS_1']) + ' ' + E(part['CS_2']) + ' ' + E(part['CS_3']) + ' ' + E(part['CS_4']) + ' ' + E(part['CS_5']) + ' ' + E(part['SHIFT_S']) +nl 
			out +=  E(part['OMEGA_S']) + ' ' + E(part['THETA_S']) + ' ' + E(part['R1_S']) + ' ' + E(part['U1_S']) + ' ' + E(part['U2_S']) + ' ' + E(part['R2_S']) +nl 
			out +=  E(part['G0_L']) + ' ' + E(part['KAPPA_L']) +nl 
			out +=  I(part['NCL']) + ' ' + E(part['CL_0']) + ' ' + E(part['CL_1']) + ' ' + E(part['CL_2']) + ' ' + E(part['CL_3']) + ' ' + E(part['CL_4']) + ' ' + E(part['CL_5']) + ' ' + E(part['SHIFT_L']) +nl 
			out +=  E(part['OMEGA_L']) + ' ' + E(part['THETA_L']) + ' ' + E(part['R1_L']) + ' ' + E(part['U1_L']) + ' ' + E(part['U2_L']) + ' ' + E(part['R2_L']) + ' ' + E(part['R3']) +nl 
		out +=  E(self._params['KIRD']) + ' ' + I(self._params['RESOL']) +nl 
		out +=  E(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) + ' ' + E(self._params['RE']) + ' ' + E(self._params['TE']) + ' ' + E(self._params['RS']) + ' ' + E(self._params['TS']) +nl 
		return out
	def add(self, **settings):
		params = {}
		params['ACN']=0
		params['DELTA_RM']=0
		params['B_0']=0
		params['IND']=0
		params['BCOEF1']=0
		params['BCOEF2']=0
		params['BCOEF3']=0
		params['BCOEF4']=0
		params['BCOEF5']=0
		params['BCOEF6']=0
		params['BCOEF7']=0
		params['BCOEF8']=0
		params['BCOEF9']=0
		params['BCOEF10']=0
		params['G0_E']=0
		params['KAPPA_E']=0
		params['NCE']=0
		params['CE_0']=0
		params['CE_1']=0
		params['CE_2']=0
		params['CE_3']=0
		params['CE_4']=0
		params['CE_5']=0
		params['SHIFT_E']=0
		params['OMEGA_E']=0
		params['THETA_E']=0
		params['R1_E']=0
		params['U1_E']=0
		params['U2_E']=0
		params['R2_E']=0
		params['G0_S']=0
		params['KAPPA_S']=0
		params['NCS']=0
		params['CS_0']=0
		params['CS_1']=0
		params['CS_2']=0
		params['CS_3']=0
		params['CS_4']=0
		params['CS_5']=0
		params['SHIFT_S']=0
		params['OMEGA_S']=0
		params['THETA_S']=0
		params['R1_S']=0
		params['U1_S']=0
		params['U2_S']=0
		params['R2_S']=0
		params['G0_L']=0
		params['KAPPA_L']=0
		params['NCL']=0
		params['CL_0']=0
		params['CL_1']=0
		params['CL_2']=0
		params['CL_3']=0
		params['CL_4']=0
		params['CL_5']=0
		params['SHIFT_L']=0
		params['OMEGA_L']=0
		params['THETA_L']=0
		params['R1_L']=0
		params['U1_L']=0
		params['U2_L']=0
		params['R2_L']=0
		params['R3']=0
		for k, v in settings.items():
			if not params.has_key(k):
				raise ValueError('Sub element of %s does not have parameter %s'%(self._class_name, k))
			params[k] = v
		self._looped_data.append(params)
		self._params['N'] = len(self._looped_data)
	def clear(self):
		self._looped_data = []

class DIPOLE(zgoubi_element):
	_class_name='DIPOLE'
	_zgoubi_name='DIPOLE'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IL']=0
		self._types['IL']='I'
		self._params['AT']=0
		self._types['AT']='E'
		self._params['RM']=0
		self._types['RM']='E'
		self._params['ACN']=0
		self._types['ACN']='E'
		self._params['B_0']=0
		self._types['B_0']='E'
		self._params['N']=0
		self._types['N']='E'
		self._params['B']=0
		self._types['B']='E'
		self._params['G']=0
		self._types['G']='E'
		self._params['LAM_E']=0
		self._types['LAM_E']='E'
		self._params['XI_E']=0
		self._types['XI_E']='E'
		self._params['NCE']=0
		self._types['NCE']='I'
		self._params['CE_0']=0
		self._types['CE_0']='E'
		self._params['CE_1']=0
		self._types['CE_1']='E'
		self._params['CE_2']=0
		self._types['CE_2']='E'
		self._params['CE_3']=0
		self._types['CE_3']='E'
		self._params['CE_4']=0
		self._types['CE_4']='E'
		self._params['CE_5']=0
		self._types['CE_5']='E'
		self._params['SHIFT_E']=0
		self._types['SHIFT_E']='E'
		self._params['OMEGA_E']=0
		self._types['OMEGA_E']='E'
		self._params['THETA_E']=0
		self._types['THETA_E']='E'
		self._params['R1_E']=0
		self._types['R1_E']='E'
		self._params['U1_E']=0
		self._types['U1_E']='E'
		self._params['U2_E']=0
		self._types['U2_E']='E'
		self._params['R2_E']=0
		self._types['R2_E']='E'
		self._params['LAM_S']=0
		self._types['LAM_S']='E'
		self._params['XI_S']=0
		self._types['XI_S']='E'
		self._params['NCS']=0
		self._types['NCS']='I'
		self._params['CS_0']=0
		self._types['CS_0']='E'
		self._params['CS_1']=0
		self._types['CS_1']='E'
		self._params['CS_2']=0
		self._types['CS_2']='E'
		self._params['CS_3']=0
		self._types['CS_3']='E'
		self._params['CS_4']=0
		self._types['CS_4']='E'
		self._params['CS_5']=0
		self._types['CS_5']='E'
		self._params['SHIFT_S']=0
		self._types['SHIFT_S']='E'
		self._params['OMEGA_S']=0
		self._types['OMEGA_S']='E'
		self._params['THETA_S']=0
		self._types['THETA_S']='E'
		self._params['R1_S']=0
		self._types['R1_S']='E'
		self._params['U1_S']=0
		self._types['U1_S']='E'
		self._params['U2_S']=0
		self._types['U2_S']='E'
		self._params['R2_S']=0
		self._types['R2_S']='E'
		self._params['LAM_L']=0
		self._types['LAM_L']='E'
		self._params['XI_L']=0
		self._types['XI_L']='E'
		self._params['NCL']=0
		self._types['NCL']='I'
		self._params['CL_0']=0
		self._types['CL_0']='E'
		self._params['CL_1']=0
		self._types['CL_1']='E'
		self._params['CL_2']=0
		self._types['CL_2']='E'
		self._params['CL_3']=0
		self._types['CL_3']='E'
		self._params['CL_4']=0
		self._types['CL_4']='E'
		self._params['CL_5']=0
		self._types['CL_5']='E'
		self._params['SHIFT_L']=0
		self._types['SHIFT_L']='E'
		self._params['OMEGA_L']=0
		self._types['OMEGA_L']='E'
		self._params['THETA_L']=0
		self._types['THETA_L']='E'
		self._params['R1_L']=0
		self._types['R1_L']='E'
		self._params['U1_L']=0
		self._types['U1_L']='E'
		self._params['U2_L']=0
		self._types['U2_L']='E'
		self._params['R2_L']=0
		self._types['R2_L']='E'
		self._params['R3']=0
		self._types['R3']='E'
		self._params['IORDRE']=0
		self._types['IORDRE']='I'
		self._params['Resol']=0
		self._types['Resol']='E'
		self._params['XPAS']=0
		self._types['XPAS']='E'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['RE']=0
		self._types['RE']='E'
		self._params['TE']=0
		self._types['TE']='E'
		self._params['RS']=0
		self._types['RS']='E'
		self._params['TS']=0
		self._types['TS']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'DIPOLE' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IL']) +nl 
		out +=  E(self._params['AT']) + ' ' + E(self._params['RM']) +nl 
		out +=  E(self._params['ACN']) + ' ' + E(self._params['B_0']) + ' ' + E(self._params['N']) + ' ' + E(self._params['B']) + ' ' + E(self._params['G']) +nl 
		out +=  E(self._params['LAM_E']) + ' ' + E(self._params['XI_E']) +nl 
		out +=  I(self._params['NCE']) + ' ' + E(self._params['CE_0']) + ' ' + E(self._params['CE_1']) + ' ' + E(self._params['CE_2']) + ' ' + E(self._params['CE_3']) + ' ' + E(self._params['CE_4']) + ' ' + E(self._params['CE_5']) + ' ' + E(self._params['SHIFT_E']) +nl 
		out +=  E(self._params['OMEGA_E']) + ' ' + E(self._params['THETA_E']) + ' ' + E(self._params['R1_E']) + ' ' + E(self._params['U1_E']) + ' ' + E(self._params['U2_E']) + ' ' + E(self._params['R2_E']) +nl 
		out +=  E(self._params['LAM_S']) + ' ' + E(self._params['XI_S']) +nl 
		out +=  I(self._params['NCS']) + ' ' + E(self._params['CS_0']) + ' ' + E(self._params['CS_1']) + ' ' + E(self._params['CS_2']) + ' ' + E(self._params['CS_3']) + ' ' + E(self._params['CS_4']) + ' ' + E(self._params['CS_5']) + ' ' + E(self._params['SHIFT_S']) +nl 
		out +=  E(self._params['OMEGA_S']) + ' ' + E(self._params['THETA_S']) + ' ' + E(self._params['R1_S']) + ' ' + E(self._params['U1_S']) + ' ' + E(self._params['U2_S']) + ' ' + E(self._params['R2_S']) +nl 
		out +=  E(self._params['LAM_L']) + ' ' + E(self._params['XI_L']) +nl 
		out +=  I(self._params['NCL']) + ' ' + E(self._params['CL_0']) + ' ' + E(self._params['CL_1']) + ' ' + E(self._params['CL_2']) + ' ' + E(self._params['CL_3']) + ' ' + E(self._params['CL_4']) + ' ' + E(self._params['CL_5']) + ' ' + E(self._params['SHIFT_L']) +nl 
		out +=  E(self._params['OMEGA_L']) + ' ' + E(self._params['THETA_L']) + ' ' + E(self._params['R1_L']) + ' ' + E(self._params['U1_L']) + ' ' + E(self._params['U2_L']) + ' ' + E(self._params['R2_L']) + ' ' + E(self._params['R3']) +nl 
		out +=  I(self._params['IORDRE']) + ' ' + E(self._params['Resol']) +nl 
		out +=  E(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) + ' ' + E(self._params['RE']) + ' ' + E(self._params['TE']) + ' ' + E(self._params['RS']) + ' ' + E(self._params['TS']) +nl 
		return out

class DRIFT(zgoubi_element):
	_class_name='DRIFT'
	_zgoubi_name='DRIFT'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['XL']=0
		self._types['XL']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'DRIFT' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  E(self._params['XL']) +nl 
		return out

class END(zgoubi_element):
	_class_name='END'
	_zgoubi_name='END'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'END' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		return out

class FAISCEAU(zgoubi_element):
	_class_name='FAISCEAU'
	_zgoubi_name='FAISCEAU'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'FAISCEAU' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		return out

class FAISCNL(zgoubi_element):
	_class_name='FAISCNL'
	_zgoubi_name='FAISCNL'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['FNAME']=''
		self._types['FNAME']='A80'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'FAISCNL' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  A(self._params['FNAME']) +nl 
		return out

class FAISTORE(zgoubi_element):
	_class_name='FAISTORE'
	_zgoubi_name='FAISTORE'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['FNAME']=''
		self._types['FNAME']='A80'
		self._params['LABELS']=''
		self._types['LABELS']='A1000'
		self._params['IP']=0
		self._types['IP']='I'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'FAISTORE' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  A(self._params['FNAME']) + ' ' + A(self._params['LABELS']) +nl 
		out +=  I(self._params['IP']) +nl 
		return out

class FFAG(zgoubi_element):
	_class_name='FFAG'
	_zgoubi_name='FFAG'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IL']=0
		self._types['IL']='I'
		self._params['N']=0
		self._types['N']='I'
		self._params['AT']=0
		self._types['AT']='E'
		self._params['RM']=0
		self._types['RM']='E'
		self._types['ACN']='E'
		self._types['DELTA_RM']='E'
		self._types['BZ_0']='E'
		self._types['K']='E'
		self._types['G0_E']='E'
		self._types['KAPPA_E']='E'
		self._types['NCE']='I'
		self._types['CE_0']='E'
		self._types['CE_1']='E'
		self._types['CE_2']='E'
		self._types['CE_3']='E'
		self._types['CE_4']='E'
		self._types['CE_5']='E'
		self._types['SHIFT_E']='E'
		self._types['OMEGA_E']='E'
		self._types['THETA_E']='E'
		self._types['R1_E']='E'
		self._types['U1_E']='E'
		self._types['U2_E']='E'
		self._types['R2_E']='E'
		self._types['G0_S']='E'
		self._types['KAPPA_S']='E'
		self._types['NCS']='I'
		self._types['CS_0']='E'
		self._types['CS_1']='E'
		self._types['CS_2']='E'
		self._types['CS_3']='E'
		self._types['CS_4']='E'
		self._types['CS_5']='E'
		self._types['SHIFT_S']='E'
		self._types['OMEGA_S']='E'
		self._types['THETA_S']='E'
		self._types['R1_S']='E'
		self._types['U1_S']='E'
		self._types['U2_S']='E'
		self._types['R2_S']='E'
		self._types['G0_L']='E'
		self._types['KAPPA_L']='E'
		self._types['NCL']='I'
		self._types['CL_0']='E'
		self._types['CL_1']='E'
		self._types['CL_2']='E'
		self._types['CL_3']='E'
		self._types['CL_4']='E'
		self._types['CL_5']='E'
		self._types['SHIFT_L']='E'
		self._types['OMEGA_L']='E'
		self._types['THETA_L']='E'
		self._types['R1_L']='E'
		self._types['U1_L']='E'
		self._types['U2_L']='E'
		self._types['R2_L']='E'
		self._params['KIRD']=0
		self._types['KIRD']='I'
		self._params['RESOL']=0
		self._types['RESOL']='I'
		self._params['XPAS']=0
		self._types['XPAS']='E'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['RE']=0
		self._types['RE']='E'
		self._params['TE']=0
		self._types['TE']='E'
		self._params['RS']=0
		self._types['RS']='E'
		self._params['TS']=0
		self._types['TS']='E'
		self.set(settings)
		self._looped_data = []
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'FFAG' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IL']) +nl 
		out +=  I(self._params['N']) + ' ' + E(self._params['AT']) + ' ' + E(self._params['RM']) +nl 
		for part in self._looped_data:
			out +=  E(part['ACN']) + ' ' + E(part['DELTA_RM']) + ' ' + E(part['BZ_0']) + ' ' + E(part['K']) +nl 
			out +=  E(part['G0_E']) + ' ' + E(part['KAPPA_E']) +nl 
			out +=  I(part['NCE']) + ' ' + E(part['CE_0']) + ' ' + E(part['CE_1']) + ' ' + E(part['CE_2']) + ' ' + E(part['CE_3']) + ' ' + E(part['CE_4']) + ' ' + E(part['CE_5']) + ' ' + E(part['SHIFT_E']) +nl 
			out +=  E(part['OMEGA_E']) + ' ' + E(part['THETA_E']) + ' ' + E(part['R1_E']) + ' ' + E(part['U1_E']) + ' ' + E(part['U2_E']) + ' ' + E(part['R2_E']) +nl 
			out +=  E(part['G0_S']) + ' ' + E(part['KAPPA_S']) +nl 
			out +=  I(part['NCS']) + ' ' + E(part['CS_0']) + ' ' + E(part['CS_1']) + ' ' + E(part['CS_2']) + ' ' + E(part['CS_3']) + ' ' + E(part['CS_4']) + ' ' + E(part['CS_5']) + ' ' + E(part['SHIFT_S']) +nl 
			out +=  E(part['OMEGA_S']) + ' ' + E(part['THETA_S']) + ' ' + E(part['R1_S']) + ' ' + E(part['U1_S']) + ' ' + E(part['U2_S']) + ' ' + E(part['R2_S']) +nl 
			out +=  E(part['G0_L']) + ' ' + E(part['KAPPA_L']) +nl 
			out +=  I(part['NCL']) + ' ' + E(part['CL_0']) + ' ' + E(part['CL_1']) + ' ' + E(part['CL_2']) + ' ' + E(part['CL_3']) + ' ' + E(part['CL_4']) + ' ' + E(part['CL_5']) + ' ' + E(part['SHIFT_L']) +nl 
			out +=  E(part['OMEGA_L']) + ' ' + E(part['THETA_L']) + ' ' + E(part['R1_L']) + ' ' + E(part['U1_L']) + ' ' + E(part['U2_L']) + ' ' + E(part['R2_L']) +nl 
		out +=  I(self._params['KIRD']) + ' ' + I(self._params['RESOL']) +nl 
		out +=  E(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) + ' ' + E(self._params['RE']) + ' ' + E(self._params['TE']) + ' ' + E(self._params['RS']) + ' ' + E(self._params['TS']) +nl 
		return out
	def add(self, **settings):
		params = {}
		params['ACN']=0
		params['DELTA_RM']=0
		params['BZ_0']=0
		params['K']=0
		params['G0_E']=0
		params['KAPPA_E']=0
		params['NCE']=0
		params['CE_0']=0
		params['CE_1']=0
		params['CE_2']=0
		params['CE_3']=0
		params['CE_4']=0
		params['CE_5']=0
		params['SHIFT_E']=0
		params['OMEGA_E']=0
		params['THETA_E']=0
		params['R1_E']=0
		params['U1_E']=0
		params['U2_E']=0
		params['R2_E']=0
		params['G0_S']=0
		params['KAPPA_S']=0
		params['NCS']=0
		params['CS_0']=0
		params['CS_1']=0
		params['CS_2']=0
		params['CS_3']=0
		params['CS_4']=0
		params['CS_5']=0
		params['SHIFT_S']=0
		params['OMEGA_S']=0
		params['THETA_S']=0
		params['R1_S']=0
		params['U1_S']=0
		params['U2_S']=0
		params['R2_S']=0
		params['G0_L']=0
		params['KAPPA_L']=0
		params['NCL']=0
		params['CL_0']=0
		params['CL_1']=0
		params['CL_2']=0
		params['CL_3']=0
		params['CL_4']=0
		params['CL_5']=0
		params['SHIFT_L']=0
		params['OMEGA_L']=0
		params['THETA_L']=0
		params['R1_L']=0
		params['U1_L']=0
		params['U2_L']=0
		params['R2_L']=0
		for k, v in settings.items():
			if not params.has_key(k):
				raise ValueError('Sub element of %s does not have parameter %s'%(self._class_name, k))
			params[k] = v
		self._looped_data.append(params)
		self._params['N'] = len(self._looped_data)
	def clear(self):
		self._looped_data = []

class MARKER(zgoubi_element):
	_class_name='MARKER'
	_zgoubi_name='MARKER'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'MARKER' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		return out

class MATRIX(zgoubi_element):
	_class_name='MATRIX'
	_zgoubi_name='MATRIX'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IORD']=0
		self._types['IORD']='I'
		self._params['IFOC']=0
		self._types['IFOC']='I'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'MATRIX' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IORD']) + ' ' + I(self._params['IFOC']) +nl 
		return out

class MCDESINT(zgoubi_element):
	_class_name='MCDESINT'
	_zgoubi_name='MCDESINT'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['M2']=0
		self._types['M2']='E'
		self._params['M3']=0
		self._types['M3']='E'
		self._params['I1']=0
		self._types['I1']='I'
		self._params['I2']=0
		self._types['I2']='I'
		self._params['I3']=0
		self._types['I3']='I'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'MCDESINT' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  E(self._params['M2']) + ' ' + E(self._params['M3']) +nl 
		out +=  I(self._params['I1']) + ' ' + I(self._params['I2']) + ' ' + I(self._params['I3']) +nl 
		return out

class MULTIPOL(zgoubi_element):
	_class_name='MULTIPOL'
	_zgoubi_name='MULTIPOL'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IL']=0
		self._types['IL']='I'
		self._params['XL']=0
		self._types['XL']='E'
		self._params['R_0']=0
		self._types['R_0']='E'
		self._params['B_1']=0
		self._types['B_1']='E'
		self._params['B_2']=0
		self._types['B_2']='E'
		self._params['B_3']=0
		self._types['B_3']='E'
		self._params['B_4']=0
		self._types['B_4']='E'
		self._params['B_5']=0
		self._types['B_5']='E'
		self._params['B_6']=0
		self._types['B_6']='E'
		self._params['B_7']=0
		self._types['B_7']='E'
		self._params['B_8']=0
		self._types['B_8']='E'
		self._params['B_9']=0
		self._types['B_9']='E'
		self._params['B_10']=0
		self._types['B_10']='E'
		self._params['X_E']=0
		self._types['X_E']='E'
		self._params['LAM_E']=0
		self._types['LAM_E']='E'
		self._params['E_2']=0
		self._types['E_2']='E'
		self._params['E_3']=0
		self._types['E_3']='E'
		self._params['E_4']=0
		self._types['E_4']='E'
		self._params['E_5']=0
		self._types['E_5']='E'
		self._params['E_6']=0
		self._types['E_6']='E'
		self._params['E_7']=0
		self._types['E_7']='E'
		self._params['E_8']=0
		self._types['E_8']='E'
		self._params['E_9']=0
		self._types['E_9']='E'
		self._params['E_10']=0
		self._types['E_10']='E'
		self._params['NCE']=0
		self._types['NCE']='I'
		self._params['C_0']=0
		self._types['C_0']='E'
		self._params['C_1']=0
		self._types['C_1']='E'
		self._params['C_2']=0
		self._types['C_2']='E'
		self._params['C_3']=0
		self._types['C_3']='E'
		self._params['C_4']=0
		self._types['C_4']='E'
		self._params['C_5']=0
		self._types['C_5']='E'
		self._params['X_S']=0
		self._types['X_S']='E'
		self._params['LAM_S']=0
		self._types['LAM_S']='E'
		self._params['S_2']=0
		self._types['S_2']='E'
		self._params['S_3']=0
		self._types['S_3']='E'
		self._params['S_4']=0
		self._types['S_4']='E'
		self._params['S_5']=0
		self._types['S_5']='E'
		self._params['S_6']=0
		self._types['S_6']='E'
		self._params['S_7']=0
		self._types['S_7']='E'
		self._params['S_8']=0
		self._types['S_8']='E'
		self._params['S_9']=0
		self._types['S_9']='E'
		self._params['S_10']=0
		self._types['S_10']='E'
		self._params['NCS']=0
		self._types['NCS']='I'
		self._params['CS_0']=0
		self._types['CS_0']='E'
		self._params['CS_1']=0
		self._types['CS_1']='E'
		self._params['CS_2']=0
		self._types['CS_2']='E'
		self._params['CS_3']=0
		self._types['CS_3']='E'
		self._params['CS_4']=0
		self._types['CS_4']='E'
		self._params['CS_5']=0
		self._types['CS_5']='E'
		self._params['R_1']=0
		self._types['R_1']='E'
		self._params['R_2']=0
		self._types['R_2']='E'
		self._params['R_3']=0
		self._types['R_3']='E'
		self._params['R_4']=0
		self._types['R_4']='E'
		self._params['R_5']=0
		self._types['R_5']='E'
		self._params['R_6']=0
		self._types['R_6']='E'
		self._params['R_7']=0
		self._types['R_7']='E'
		self._params['R_8']=0
		self._types['R_8']='E'
		self._params['R_9']=0
		self._types['R_9']='E'
		self._params['R_10']=0
		self._types['R_10']='E'
		self._params['XPAS']=0
		self._types['XPAS']='X'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['XCE']=0
		self._types['XCE']='E'
		self._params['YCE']=0
		self._types['YCE']='E'
		self._params['ALE']=0
		self._types['ALE']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'MULTIPOL' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IL']) +nl 
		out +=  E(self._params['XL']) + ' ' + E(self._params['R_0']) + ' ' + E(self._params['B_1']) + ' ' + E(self._params['B_2']) + ' ' + E(self._params['B_3']) + ' ' + E(self._params['B_4']) + ' ' + E(self._params['B_5']) + ' ' + E(self._params['B_6']) + ' ' + E(self._params['B_7']) + ' ' + E(self._params['B_8']) + ' ' + E(self._params['B_9']) + ' ' + E(self._params['B_10']) +nl 
		out +=  E(self._params['X_E']) + ' ' + E(self._params['LAM_E']) + ' ' + E(self._params['E_2']) + ' ' + E(self._params['E_3']) + ' ' + E(self._params['E_4']) + ' ' + E(self._params['E_5']) + ' ' + E(self._params['E_6']) + ' ' + E(self._params['E_7']) + ' ' + E(self._params['E_8']) + ' ' + E(self._params['E_9']) + ' ' + E(self._params['E_10']) +nl 
		out +=  I(self._params['NCE']) + ' ' + E(self._params['C_0']) + ' ' + E(self._params['C_1']) + ' ' + E(self._params['C_2']) + ' ' + E(self._params['C_3']) + ' ' + E(self._params['C_4']) + ' ' + E(self._params['C_5']) +nl 
		out +=  E(self._params['X_S']) + ' ' + E(self._params['LAM_S']) + ' ' + E(self._params['S_2']) + ' ' + E(self._params['S_3']) + ' ' + E(self._params['S_4']) + ' ' + E(self._params['S_5']) + ' ' + E(self._params['S_6']) + ' ' + E(self._params['S_7']) + ' ' + E(self._params['S_8']) + ' ' + E(self._params['S_9']) + ' ' + E(self._params['S_10']) +nl 
		out +=  I(self._params['NCS']) + ' ' + E(self._params['CS_0']) + ' ' + E(self._params['CS_1']) + ' ' + E(self._params['CS_2']) + ' ' + E(self._params['CS_3']) + ' ' + E(self._params['CS_4']) + ' ' + E(self._params['CS_5']) +nl 
		out +=  E(self._params['R_1']) + ' ' + E(self._params['R_2']) + ' ' + E(self._params['R_3']) + ' ' + E(self._params['R_4']) + ' ' + E(self._params['R_5']) + ' ' + E(self._params['R_6']) + ' ' + E(self._params['R_7']) + ' ' + E(self._params['R_8']) + ' ' + E(self._params['R_9']) + ' ' + E(self._params['R_10']) +nl 
		out +=  X(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) + ' ' + E(self._params['XCE']) + ' ' + E(self._params['YCE']) + ' ' + E(self._params['ALE']) +nl 
		return out

class ORDRE(zgoubi_element):
	_class_name='ORDRE'
	_zgoubi_name='ORDRE'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IO']=0
		self._types['IO']='I'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'ORDRE' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IO']) +nl 
		return out

class PARTICUL(zgoubi_element):
	_class_name='PARTICUL'
	_zgoubi_name='PARTICUL'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['M']=0
		self._types['M']='E'
		self._params['Q']=0
		self._types['Q']='E'
		self._params['G']=0
		self._types['G']='E'
		self._params['tau']=0
		self._types['tau']='E'
		self._params['X']=0
		self._types['X']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'PARTICUL' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  E(self._params['M']) + ' ' + E(self._params['Q']) + ' ' + E(self._params['G']) + ' ' + E(self._params['tau']) + ' ' + E(self._params['X']) +nl 
		return out

class POLARMES(zgoubi_element):
	_class_name='POLARMES'
	_zgoubi_name='POLARMES'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IC']=0
		self._types['IC']='I'
		self._params['IL']=0
		self._types['IL']='I'
		self._params['BNORM']=0
		self._types['BNORM']='E'
		self._params['AN']=0
		self._types['AN']='E'
		self._params['RN']=0
		self._types['RN']='E'
		self._params['TITL']=''
		self._types['TITL']='A80'
		self._params['IA']=0
		self._types['IA']='I'
		self._params['JR']=0
		self._types['JR']='I'
		self._params['FNAME']=''
		self._types['FNAME']='A80'
		self._params['ID']=0
		self._types['ID']='I'
		self._params['A']=0
		self._types['A']='E'
		self._params['B']=0
		self._types['B']='E'
		self._params['C']=0
		self._types['C']='E'
		self._params['IORDRE']=0
		self._types['IORDRE']='I'
		self._params['XPAS']=0
		self._types['XPAS']='E'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['RE']=0
		self._types['RE']='E'
		self._params['TE']=0
		self._types['TE']='E'
		self._params['RS']=0
		self._types['RS']='E'
		self._params['TS']=0
		self._types['TS']='E'
		self._params['DP']=0
		self._types['DP']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'POLARMES' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IC']) + ' ' + I(self._params['IL']) +nl 
		out +=  E(self._params['BNORM']) + ' ' + E(self._params['AN']) + ' ' + E(self._params['RN']) +nl 
		out +=  A(self._params['TITL']) +nl 
		out +=  I(self._params['IA']) + ' ' + I(self._params['JR']) +nl 
		out +=  A(self._params['FNAME']) +nl 
		out +=  I(self._params['ID']) + ' ' + E(self._params['A']) + ' ' + E(self._params['B']) + ' ' + E(self._params['C']) +nl 
		out +=  I(self._params['IORDRE']) +nl 
		out +=  E(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) +nl 
		if self._params['KPOS'] == 2 : out +=  E(self._params['RE']) + ' ' + E(self._params['TE']) + ' ' + E(self._params['RS']) + ' ' + E(self._params['TS']) +nl 
		if self._params['KPOS'] == 1 : out +=  E(self._params['DP']) +nl 
		return out

class QUADRUPO(zgoubi_element):
	_class_name='QUADRUPO'
	_zgoubi_name='QUADRUPO'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IL']=0
		self._types['IL']='I'
		self._params['XL']=0
		self._types['XL']='E'
		self._params['R_0']=0
		self._types['R_0']='E'
		self._params['B_0']=0
		self._types['B_0']='E'
		self._params['X_E']=0
		self._types['X_E']='E'
		self._params['LAM_E']=0
		self._types['LAM_E']='E'
		self._params['NCE']=0
		self._types['NCE']='I'
		self._params['C_0']=0
		self._types['C_0']='E'
		self._params['C_1']=0
		self._types['C_1']='E'
		self._params['C_2']=0
		self._types['C_2']='E'
		self._params['C_3']=0
		self._types['C_3']='E'
		self._params['C_4']=0
		self._types['C_4']='E'
		self._params['C_5']=0
		self._types['C_5']='E'
		self._params['X_S']=0
		self._types['X_S']='E'
		self._params['LAM_S']=0
		self._types['LAM_S']='E'
		self._params['NCS']=0
		self._types['NCS']='I'
		self._params['CS_0']=0
		self._types['CS_0']='E'
		self._params['CS_1']=0
		self._types['CS_1']='E'
		self._params['CS_2']=0
		self._types['CS_2']='E'
		self._params['CS_3']=0
		self._types['CS_3']='E'
		self._params['CS_4']=0
		self._types['CS_4']='E'
		self._params['CS_5']=0
		self._types['CS_5']='E'
		self._params['XPAS']=0
		self._types['XPAS']='X'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['XCE']=0
		self._types['XCE']='E'
		self._params['YCE']=0
		self._types['YCE']='E'
		self._params['ALE']=0
		self._types['ALE']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'QUADRUPO' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IL']) +nl 
		out +=  E(self._params['XL']) + ' ' + E(self._params['R_0']) + ' ' + E(self._params['B_0']) +nl 
		out +=  E(self._params['X_E']) + ' ' + E(self._params['LAM_E']) +nl 
		out +=  I(self._params['NCE']) + ' ' + E(self._params['C_0']) + ' ' + E(self._params['C_1']) + ' ' + E(self._params['C_2']) + ' ' + E(self._params['C_3']) + ' ' + E(self._params['C_4']) + ' ' + E(self._params['C_5']) +nl 
		out +=  E(self._params['X_S']) + ' ' + E(self._params['LAM_S']) +nl 
		out +=  I(self._params['NCS']) + ' ' + E(self._params['CS_0']) + ' ' + E(self._params['CS_1']) + ' ' + E(self._params['CS_2']) + ' ' + E(self._params['CS_3']) + ' ' + E(self._params['CS_4']) + ' ' + E(self._params['CS_5']) +nl 
		out +=  X(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) + ' ' + E(self._params['XCE']) + ' ' + E(self._params['YCE']) + ' ' + E(self._params['ALE']) +nl 
		return out

class REBELOTE(zgoubi_element):
	_class_name='REBELOTE'
	_zgoubi_name='REBELOTE'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['NPASS']=0
		self._types['NPASS']='I'
		self._params['KWRIT']=0
		self._types['KWRIT']='I'
		self._params['K']=0
		self._types['K']='I'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'REBELOTE' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['NPASS']) + ' ' + I(self._params['KWRIT']) + ' ' + I(self._params['K']) +nl 
		return out

class SCALING(zgoubi_element):
	_class_name='SCALING'
	_zgoubi_name='SCALING'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IOPT']=0
		self._types['IOPT']='I'
		self._params['NFAM']=0
		self._types['NFAM']='I'
		self._params['NAMEF']=''
		self._types['NAMEF']='A80'
		self._params['NT']=0
		self._types['NT']='I'
		self._params['SCL']=0
		self._types['SCL']='E'
		self._params['TIM']=0
		self._types['TIM']='I'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'SCALING' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IOPT']) + ' ' + I(self._params['NFAM']) +nl 
		out +=  A(self._params['NAMEF']) +nl 
		out +=  I(self._params['NT']) +nl 
		out +=  E(self._params['SCL']) +nl 
		out +=  I(self._params['TIM']) +nl 
		return out

class SPNPRNL(zgoubi_element):
	_class_name='SPNPRNL'
	_zgoubi_name='SPNPRNL'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['FNAME']=''
		self._types['FNAME']='A80'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'SPNPRNL' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  A(self._params['FNAME']) +nl 
		return out

class SPNPRT(zgoubi_element):
	_class_name='SPNPRT'
	_zgoubi_name='SPNPRT'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'SPNPRT' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		return out

class SPNSTORE(zgoubi_element):
	_class_name='SPNSTORE'
	_zgoubi_name='SPNSTORE'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['FNAME']=''
		self._types['FNAME']='A80'
		self._params['LABELS']=''
		self._types['LABELS']='A1000'
		self._params['IP']=0
		self._types['IP']='I'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'SPNSTORE' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  A(self._params['FNAME']) + ' ' + A(self._params['LABELS']) +nl 
		out +=  I(self._params['IP']) +nl 
		return out

class TOSCA(zgoubi_element):
	_class_name='TOSCA'
	_zgoubi_name='TOSCA'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IC']=0
		self._types['IC']='I'
		self._params['IL']=0
		self._types['IL']='I'
		self._params['BNORM']=0
		self._types['BNORM']='E'
		self._params['XN']=0
		self._types['XN']='E'
		self._params['YN']=0
		self._types['YN']='E'
		self._params['ZN']=0
		self._types['ZN']='E'
		self._params['TIT']=''
		self._types['TIT']='A80'
		self._params['IX']=0
		self._types['IX']='I'
		self._params['IY']=0
		self._types['IY']='I'
		self._params['IZ']=0
		self._types['IZ']='I'
		self._params['MOD']=0
		self._types['MOD']='I'
		self._params['FNAME']=''
		self._types['FNAME']='A8000'
		self._params['ID']=0
		self._types['ID']='I'
		self._params['A']=0
		self._types['A']='E'
		self._params['B']=0
		self._types['B']='E'
		self._params['C']=0
		self._types['C']='E'
		self._params['Ap']=0
		self._types['Ap']='E'
		self._params['Bp']=0
		self._types['Bp']='E'
		self._params['Cp']=0
		self._types['Cp']='E'
		self._params['App']=0
		self._types['App']='E'
		self._params['Bpp']=0
		self._types['Bpp']='E'
		self._params['Cpp']=0
		self._types['Cpp']='E'
		self._params['IORDRE']=0
		self._types['IORDRE']='I'
		self._params['XPAS']=0
		self._types['XPAS']='X'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['XCE']=0
		self._types['XCE']='E'
		self._params['YCE']=0
		self._types['YCE']='E'
		self._params['ALE']=0
		self._types['ALE']='E'
		self._params['RE']=0
		self._types['RE']='E'
		self._params['TE']=0
		self._types['TE']='E'
		self._params['RS']=0
		self._types['RS']='E'
		self._params['TS']=0
		self._types['TS']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'TOSCA' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IC']) + ' ' + I(self._params['IL']) +nl 
		out +=  E(self._params['BNORM']) + ' ' + E(self._params['XN']) + ' ' + E(self._params['YN']) + ' ' + E(self._params['ZN']) +nl 
		out +=  A(self._params['TIT']) +nl 
		out +=  I(self._params['IX']) + ' ' + I(self._params['IY']) + ' ' + I(self._params['IZ']) + ' ' + I(self._params['MOD']) +nl 
		out +=  A(self._params['FNAME']) +nl 
		out +=  I(self._params['ID']) + ' ' + E(self._params['A']) + ' ' + E(self._params['B']) + ' ' + E(self._params['C']) + ' ' + E(self._params['Ap']) + ' ' + E(self._params['Bp']) + ' ' + E(self._params['Cp']) + ' ' + E(self._params['App']) + ' ' + E(self._params['Bpp']) + ' ' + E(self._params['Cpp']) +nl 
		out +=  I(self._params['IORDRE']) +nl 
		out +=  X(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) +nl 
		if self._params['KPOS'] == 1 : out +=  E(self._params['XCE']) + ' ' + E(self._params['YCE']) + ' ' + E(self._params['ALE']) +nl 
		if self._params['KPOS'] == 2 : out +=  E(self._params['RE']) + ' ' + E(self._params['TE']) + ' ' + E(self._params['RS']) + ' ' + E(self._params['TS']) +nl 
		return out

class UNIPOT(zgoubi_element):
	_class_name='UNIPOT'
	_zgoubi_name='UNIPOT'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self._params['IL']=0
		self._types['IL']='I'
		self._params['X1']=0
		self._types['X1']='E'
		self._params['D']=0
		self._types['D']='E'
		self._params['X2']=0
		self._types['X2']='E'
		self._params['X3']=0
		self._types['X3']='E'
		self._params['R0']=0
		self._types['R0']='E'
		self._params['V1']=0
		self._types['V1']='E'
		self._params['V2']=0
		self._types['V2']='E'
		self._params['XPAS']=0
		self._types['XPAS']='E'
		self._params['KPOS']=0
		self._types['KPOS']='I'
		self._params['XCE']=0
		self._types['XCE']='E'
		self._params['YCE']=0
		self._types['YCE']='E'
		self._params['ALE']=0
		self._types['ALE']='E'
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'UNIPOT' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		out +=  I(self._params['IL']) +nl 
		out +=  E(self._params['X1']) + ' ' + E(self._params['D']) + ' ' + E(self._params['X2']) + ' ' + E(self._params['X3']) + ' ' + E(self._params['R0']) +nl 
		out +=  E(self._params['V1']) + ' ' + E(self._params['V2']) +nl 
		out +=  E(self._params['XPAS']) +nl 
		out +=  I(self._params['KPOS']) + ' ' + E(self._params['XCE']) + ' ' + E(self._params['YCE']) + ' ' + E(self._params['ALE']) +nl 
		return out

class YMY(zgoubi_element):
	_class_name='YMY'
	_zgoubi_name='YMY'
	def __init__(self, label1='', label2='', **settings):
		self._params={}
		self._types={}
		self._params['label1'] = label1
		self._params['label2'] = label2
		self.set(settings)
	def output(self):
		I=self.i2s
		E=self.f2s
		A=str
		X=self.x2s
		out = ''
		nl = '\n'
		sq = '\''
		out += sq + 'YMY' + sq + ' ' + self._params['label1'][:8] + ' ' + self._params['label2'][:8]  + nl 
		return out

