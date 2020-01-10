from pyomo.environ import *
from pyomo.core.base.block import generate_cuid_names
from pyomo.opt import SolverStatus, TerminationCondition
import sys


def get_solver_path(solver="cplex"):
    """
    Returns the absolute path to a given solver.
    Expects a parent directory to contain a directory ampl or AMPL that contains the solver.
    Example:
    - current folder : /home/user/optim/td1/
    - solver path : /home/user/optim/ampl/cplex
    """
    import pathlib
    p = pathlib.Path('.').absolute()

    ####check with .exe extension (for Windows)
    if isinstance(p, pathlib.WindowsPath):
        solver += ".exe"
    
    for p_dir in p.parents:
        path = p_dir.joinpath('solvers', solver)
        if path.exists():
            break
        path = p_dir.joinpath('SOLVERS', solver)
        if path.exists():
            break
    else:
        example_path = p.parents[0].joinpath('ampl', solver)
        raise OSError(
            """Cannot find the solver !

Expected to find an ampl directory in the path, e.g.
{example_path}""")
    return path

def printObjectiveExpression(model_instance, filename=None):
    """
    Prints the expression of the objective function.
    Expects a model instance (and optionally a filename)
    """
    for o in model_instance.component_objects(Objective, active=True):
        objobject = getattr(model_instance, str(o))
        print(o, "Objective expression ", objobject.expr, file=filename)
            

def printObjectiveValue(model_instance, filename=None):
    """
    Prints the value of the objective function.
    Expects a model instance (and optionally a filename)
    """
    for o in model_instance.component_objects(Objective, active=True):
        objobject = getattr(model_instance, str(o))
        print("OBJ: ", o, " = ", value(objobject), file=filename)

def getObjectiveValue(model_instance):
    """
    Returns the value of the objective function.
    Expects a model instance (and optionally a filename)
    """
    for o in model_instance.component_objects(Objective, active=True):
        objobject = getattr(model_instance, str(o))
        return value(objobject)
        
def printPointFromModel(model_instance, filename=None):
    """
    Prints all the variables' values.
    Expects a model instance (and optionally a filename)
    """
    for v in model_instance.component_objects(Var, active=True):
        varobject = getattr(model_instance, str(v))
        for index in varobject:
            print(v ,"[" ,index, "] = ", varobject[index].value, file=filename)

def printSlacks(model_instance, filename=None):
    """
    Prints all the constraints' slacks.
    Expects a model instance (and optionally a filename)
    """
    for c in model_instance.component_objects(Constraint, active=True):
        constobject = getattr(model_instance, str(c))
        for index in constobject:
            print(c ,index, constobject[index].lslack(), constobject[index].uslack(), file=filename)

def printDual(model_instance, filename=None):
    """
    Prints all the values of the dual variables.
    Expects a model instance (and optionally a filename)
    """
    for c in model_instance.component_objects(Constraint, active=True):
        print ("   Constraint",c)
        for index in c:
            if model_instance.dual[c[index]]!=None:
                print ("      ", index, model_instance.dual[c[index]], file=filename)
            else:
                print (" No dual for      ", index, file=filename)


#####################################################################
#####################################################################


def CheckBounds(model_instance, filename=None):
    for v in model_instance.component_objects(Var, active=True):
        varobject = getattr(model_instance, str(v))
        LB_Ok = 'True'
        UB_Ok = 'True'
        for index in varobject:
            if varobject[index].lb != None:
                if varobject[index].lb >varobject[index].value:
                    LB_Ok = 'False'            
            if varobject[index].ub != None:
                if varobject[index].ub.value <varobject[index].value:
                    UB_Ok = 'False'
            if LB_Ok == 'True' and UB_Ok == 'True':
                print(v ,"[" ,index, "] ", "bounds OK", file=filename)
            else:
                print(v ,"[" ,index, "] ", "outofbounds", file=filename)

def PrintBounds(model_instance, filename=None):
    for v in model_instance.component_objects(Var, active=True):
        varobject = getattr(model_instance, str(v))
        for index in varobject:
            print(value(varobject[index].lb), varobject[index], value(varobject[index].ub), file=filename)

def initZero(model_instance):
    for v in model_instance.component_objects(Var, active=True):
        varobject = getattr(model_instance, str(v))
        for index in varobject:
            varobject[index] = 0.0

def FixInteger(instance):
    for v in instance.active_components(Var):
        varobject = getattr(instance, v)
        if isinstance(varobject.domain, IntegerSet) or isinstance(varobject.domain, BooleanSet):
            print ("fixing",v)
            for index in varobject:
                varobject[index].fixed = True # fix the current value
