import sympy
from IPython.display import Math
from IPython.display import display
import copy

class BasicAlgebraicCalculationClass:

  def __init__(self, input_variable_list = []):
    '''
    Initialze object.
    Variables can be defined at __init__. In that case, insert a list of variables as first argument.
    '''
    self.left_hand_side = 'f(x)'
    self.right_hand_side = sympy.symbols("x")
    self.matrix_symbol = None
    self.matrix_element_symbols = None
    self.expanded_right_hand_side = None
    self.integrated_left_hand_side = None
    self.integrated_right_hand_side = None
    self.differentiated_left_hand_side = None
    self.differentiated_right_hand_side = None
    self.variable_list = None
    self.variable_symbols = None
    self.latex_paste_mode = False
    if len(input_variable_list) != 0:
      self.variable_list = input_variable_list
      self.variable_symbols = input_variable_list
      self.set_variable_symbols()

  def copy_class(self):
    '''
    Copy object
    '''
    return copy.copy(self)

  def select_print_mode(self, Bool):
    '''
    Select Print Mode (Default : False)
      False : Print with IPython.Display (Output is in Latex format if a jupyer notebook-based application is used.)
      True :　Print with print function(The output is in Latex formula notation.　Pasteable in overleaf or Cloud latex.)
    '''
    self.latex_paste_mode = Bool

  def set_formula(self, lhs, rhs):
    '''
    Assign left hand side and right hand side
    '''
    self.left_hand_side = lhs
    self.right_hand_side = rhs

  def set_left_hand_side(self, lhs):
    '''
    Assign left hand side
    '''
    self.left_hand_side = lhs

  def set_right_hand_side(self, rhs):
    '''
    Assign right hand side
    '''
    self.right_hand_side = rhs

  def set_variable_symbols(self, input_list=None):
    '''
    Registor the variables created by sympy.symbol to this class.
    It is used for differentiating and integrating.
    '''
    self.variable_symbols = []
    if input_list is not None:
      self.variable_list = input_list
    for i in range( len( self.variable_list ) ):
      self.variable_symbols.append( sympy.symbols( self.variable_list[i] ) )

  def get_formula(self):
    '''
    Return left hand side and right hand side
    '''
    return self.left_hand_side, self.right_hand_side

  def get_left_hand_side(self):
    '''
    Return left hand side
    '''
    return self.left_hand_side

  def get_right_hand_side(self):
    '''
    Return right hand side
    '''
    return self.right_hand_side

  def create_variables(self, input_variable_list):
    '''
    Create variables as algebra using sympy.symbols
      input_variable_list : list of variables.
    '''
    self.created_variable_symbols = []
    for i in range( len( input_variable_list ) ):
      self.created_variable_symbols.append( sympy.symbols( input_variable_list[i] ) )

    self.set_variable_symbols( input_variable_list )
    return self.created_variable_symbols

  def assign_values(self, symbol, values, round_digits=None ):
    '''
    Assign and round variables.
      symbol : list of slgebaric variables
      values : list of numerical variables
      round_digits : number of digits
    '''
    self.variable_values_args = sympy.lambdify( symbol, self.right_hand_side, "numpy" )
    if round_digits is not None:
        for i in range( len( values ) ):
            values[i] = round( values[i], int(round_digits) )
    self.variable_values = self.variable_values_args( *values )

  def get_variable_symbols(self):
    '''
    Return registered symbols
    '''
    return self.variable_symbols

  def get_variable_values(self):
    '''
    Return assigned values
    '''
    return self.variable_values

  def round_right_hand_side(self, round_digits):
    '''
    Improve readability when the formula will be dumped since the default number of digits displayed is very large.
    The rounded function is overridden by the original function.
    Therefore, it is recommended to use this function only at the end of the function output.
    In addition, the problem of +1.0 and -1.0 being displayed after rounding has been eliminated.
    (+1.0 and -1.0 when rounding with zero digits forces the assignment of +1 and -1.)
    '''
    replacements = {}
    for n in self.right_hand_side.atoms( sympy.Number ):
      val = round( n, round_digits )
      if abs( round( val, 0 ) ) == 1:
        replacements[n] = int( round( val, 0 ) )
      else:
        replacements[n] = round( n, round_digits )
    self.right_hand_side = self.right_hand_side.xreplace( replacements )
    return self.right_hand_side

  def create_martix_symbols(self, matrixsymbol, row, col, elementsymbol=None):
    '''
    Create matrix as algebra
      matrixsymbol : variable that represents the entire matrix. (recommend to use capital letter)
      row :　maximum row number
      col : maximum column number
      elementsymbol : symbol of each elements (if elementsymbol is none, lowercase letter is adpoted)
    '''
    self.matrix_symbol = []
    self.matrix_element_symbols = []
    matrix = []
    for i in range( row ):
      rowindex = "_"+str(i+1)
      row = []
      for j in range( col ):
        colindex = "_" + str(j+1)
        elements = None
        if elementsymbol is None:
          elements = matrixsymbol.lower() + rowindex+colindex
        else :
          elements = elementsymbol + rowindex + colindex
        self.matrix_element_symbols.append( sympy.symbols( elements ) )
        row.append( elements )
      matrix.append( row )
    self.matrix_symbol = sympy.Matrix( matrix )
    return self.matrix_symbol, self.matrix_element_symbols

  def print_formula(self):
    '''
    Dump formula.
    Select print mode in self.select_print_mode()
      False : Print with IPython.Display (Output is in Latex format if a jupyer notebook-based application is used.)
      True :　Print with print function(The output is in Latex formula notation.　Pasteable in overleaf or Cloud latex.)
    '''
    if not self.latex_paste_mode:
      display( Math( f'{self.left_hand_side} = {sympy.latex( self.right_hand_side )}' ) )
    elif self.latex_paste_mode:
      print(  self.left_hand_side , "=", sympy.latex( self.right_hand_side ), "\\\\" )

  def print_external_input(self, external_input_lhs=None, external_input_rhs=None):
    '''
    Dump external input
    Select print mode in self.select_print_mode()
      False : Print with IPython.Display (Output is in Latex format if a jupyer notebook-based application is used.)
      True :　Print with print function(The output is in Latex formula notation.　Pasteable in overleaf or Cloud latex.)
    '''
    dum_lhs = 'f'
    if external_input_lhs is not None:
      dum_lhs = external_input_lhs
    if external_input_rhs is not None:
      if not self.latex_paste_mode:
        display( Math( f'{dum_lhs} = {sympy.latex( external_input_rhs )}' ) )
      elif self.latex_paste_mode :
        print( dum_lhs, " = ", sympy.latex( external_input_rhs ), "\\\\" )

  def expand_formula(self, assign_flag=False):
    '''
    Expand formula.
      assign_flag : flag to update original function. (default : no update)
    '''
    self.expanded_right_hand_side = self.right_hand_side.expand()
    if not self.latex_paste_mode:
      display( Math( f'{self.left_hand_side} = {sympy.latex( self.expanded_right_hand_side )}' ) )
    elif self.latex_paste_mode:
      print( self.left_hand_side , "=", sympy.latex( self.expanded_right_hand_side ), "\\\\"  )

    if True:
      self.right_hand_side = self.expanded_right_hand_side

  def get_matrix(self, input):
    '''
    Return matrix
    '''
    return sympy.Matrix( input )

  def indefinite_integral(self, val, update_flag=False):
    '''
    Execute indefinite integral with variable called in 2nd argument.
    '''
    self.integrated_left_hand_side = '\\int ' + self.left_hand_side + 'd' + str(val)
    self.integrated_right_hand_side = sympy.integrate( self.right_hand_side, val )
    if update_flag :
      self.left_hand_side = self.integrated_left_hand_side
      self.right_hand_side = self.integrated_right_hand_side
    return self.integrated_right_hand_side

  def definite_integral(self, val, min, max, update_flag=False):
    '''
    Execute definite integral with variable called in 2nd argument from min(3rd argument) to max(4th argument).
    '''
    self.integrated_left_hand_side = '\\int_{' + str(min) + '}^{' + str(max) + '}' + self.left_hand_side + 'd' + str(val)
    self.integrated_right_hand_side = sympy.integrate( self.right_hand_side, ( val, min, max ) )
    if update_flag:
      self.left_hand_side = self.integrated_left_hand_side
      self.right_hand_side = self.integrated_right_hand_side
    return self.integrated_right_hand_side

  def differentiate(self, val, update_flag=False):
    '''
    Execute differentiate with variable called in 2nd argument.
    '''
    self.differentiated_left_hand_side = '\\frac{d}{d' + str(val) + '}' + self.left_hand_side
    self.differentiated_right_hand_side = sympy.diff( self.right_hand_side , val )
    if update_flag:
      self.left_hand_side = self.differentiated_left_hand_side
      self.right_hand_side = self.differentiated_right_hand_side
    return self.differentiated_right_hand_side

