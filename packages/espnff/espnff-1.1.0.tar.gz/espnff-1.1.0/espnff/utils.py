import numpy
import warnings


def square_matrix(X):
    '''Squares a matrix'''
    result = numpy.zeros(shape=(len(X), len(X[0])))

    # iterate through rows of X
    for i in range(len(X)):

        # iterate through columns of X
        for j in range(len(X[0])):

            # iterate through rows of X
            for k in range(len(X)):
                result[i][j] += X[i][k] * X[k][j]

    return result.tolist()


def add_matrix(X, Y):
    '''Adds two matrices'''
    result = numpy.zeros(shape=(len(X), len(X[0])))

    for i in range(len(X)):

        # iterate through columns
        for j in range(len(X[0])):
            result[i][j] = X[i][j] + Y[i][j]

    return result.tolist()


def two_step_dominance(X):
    '''Returns result of two step dominance formula'''
    matrix = add_matrix(square_matrix(X), X)
    result = [sum(x) for x in matrix]
    return result


def power_points(dominance, teams, week):
    '''Returns list of power points'''
    power_points = []
    for i, team in zip(dominance, teams):
        avg_score = sum(team.scores[:week]) / week
        avg_mov = sum(team.mov[:week]) / week

        power = '{0:.2f}'.format((int(i)*0.8) + (int(avg_score)*0.15) +
                                 (int(avg_mov)*0.05))
        power_points.append(power)
    power_tup = [(i, j) for (i, j) in zip(power_points, teams)]
    return sorted(power_tup, key=lambda tup: float(tup[0]), reverse=True)


def deprecated_property(old_name, new_name):
    def getter(self):
        warnings.warn('%s will be removed in future versions, please use %s instead.'
                      % (old_name, new_name), stacklevel=2)
        return getattr(self, new_name)

    def setter(self, value):
        warnings.warn('%s will be removed in future versions, please use %s instead.'
                      % (old_name, new_name), stacklevel=2)
        setattr(self, new_name, value)

    prop = property(getter)
    prop.setter(setter)
    return prop
