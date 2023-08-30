class comparison_conn_comp:
    def __init__(self):
        self.c_conn = 25

    def equali(self):
        self._c_comp = self.c_conn

    @property
    def c_comp(self):
        return self._c_comp

    @c_comp.setter
    def c_comp(self, c_cost):
        self._c_comp = c_cost
        self._c_conn = c_cost
    @property
    def c_conn(self):
        return self._c_conn


    @c_conn.setter
    def c_conn(self, c_cost):
        self._c_conn = c_cost
        self._c_comp = c_cost


turbine = comparison_conn_comp()

print(turbine.c_conn)
print(turbine.c_comp)

turbine.c_conn = 7
print(turbine.c_conn)
print(turbine.c_comp)

turbine.c_comp = -81
print(turbine.c_conn)
print(turbine.c_comp)
