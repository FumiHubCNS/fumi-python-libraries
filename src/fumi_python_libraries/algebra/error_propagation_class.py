import sympy
import numpy
from IPython.display import Math
from IPython.display import display
import copy
from .basic_algebraic_calculation_class import BasicAlgebraicCalculationClass

class ErrorPropagationClass( BasicAlgebraicCalculationClass ):
  def __init__(self):
    super().__init__()
    self.dfdx_symbol = None
    self.dfdx_value = None
    self.error_series = None
    self.value_series = None
    self.dfdx_value_args = None
    self.dfdx_value = None
    self.error_series_variable = None
    self.error_series_variable_pow2 = None
    self.propagated_error = None
    self.propagated_value = None
    self.original_function = None
    self.latex_paste_mode = False

  def copy_class(self):
    '''
    Copy object
    '''
    return copy.copy(self)

  def set_value_series(self, values):
    '''
    '''
    self.value_series = []
    for i in range( len( values ) ):
      self.value_series.append( values[i] )

  def set_error_series(self, evalues):
    '''
    '''
    self.error_series = []
    for i in range( len( evalues ) ):
      self.error_series.append( evalues[i] )

  def print_each_term(self, lhs, rhs, i):
    '''
    '''
    if not self.latex_paste_mode:
      display( Math( f'\\frac{{\\partial {self.left_hand_side} }}{{ \\partial {self.variable_symbols[i]} }} = {sympy.latex( self.dfdx_symbol[i] )}' ) )
    elif self.latex_paste_mode:
      print(( '\\frac{{\\partial} f}{{\\partial} x_%d}=\\frac{{\\partial}%s}{{\\partial}%s}=%s \\\\' % (i, sympy.latex(self.left_hand_side), sympy.latex( lhs ), sympy.latex( rhs ) )))

  def partial_derivative(self, dump_flag=False):
    '''
    '''
    self.dfdx_symbol = []
    if self.original_function is None:
      self.original_function = self.right_hand_side
    elif self.original_function != self.right_hand_side:
        self.original_function = self.right_hand_side
        
    if dump_flag:
      if not self.latex_paste_mode:
        display( Math( r'{\delta}f=\sqrt{\sum_{i=0}^{n} \left( \frac{{\partial} f}{{\partial} x_i} {\delta}x_i \right)^2}') )
        for i in range( len(self.variable_symbols) ):
          display( Math( f'x_{i} = {self.variable_symbols[i]}' ) )
      elif self.latex_paste_mode:
        print( f'x_{i} = {self.variable_symbols[i]}' )
    for i in range( len( self.variable_symbols ) ):
      self.dfdx_symbol.append( sympy.diff( self.right_hand_side, self.variable_symbols[i] ) )
      if dump_flag:
        self.print_each_term( self.variable_symbols[i], self.dfdx_symbol[i], i )

  def calculate_erorr(self, dump_flag=False, round_digits=None):
    '''
    '''
    calc_variable_symbols = self.variable_symbols
    calc_dfdx_symbol = self.dfdx_symbol
    calc_value_series = self.value_series
    calc_error_series = self.error_series
    calc_original_function = self.original_function

    self.assign_values( calc_variable_symbols, calc_value_series )
    self.set_right_hand_side( self.get_variable_values() )
    self.propagated_value = self.get_right_hand_side()
    self.set_right_hand_side( calc_original_function )

    self.dfdx_value_args = []
    self.dfdx_value = []
    self.error_series_variable = []
    self.error_series_variable_pow2 = []
    for i in range( len( calc_variable_symbols ) ):
      self.dfdx_value_args.append( sympy.lambdify( calc_variable_symbols, calc_dfdx_symbol[i], "numpy" ) )
      self.dfdx_value.append( self.dfdx_value_args[i]( *calc_value_series ) )
      self.error_series_variable.append( self.dfdx_value[i] * calc_error_series[i] )
      self.error_series_variable_pow2.append( self.error_series_variable[i]**2 )

    self.propagated_error = numpy.sqrt( sum( self.error_series_variable_pow2 ) )

    val_print = self.propagated_value
    err_print = self.propagated_error
    if round_digits is not None :
      val_print = round( self.propagated_value, round_digits )
      err_print = round( self.propagated_error, round_digits )

    if dump_flag:
      if not self.latex_paste_mode:
        display( Math( f'{self.left_hand_side} \\pm \\delta {self.left_hand_side} = {val_print} \\pm {err_print}' ) )
      elif self.latex_paste_mode:
        print( f'{val_print} \\pm {err_print} \\\\' )

    return self.propagated_error, self.propagated_value
