import data_simulator

n = 5000

x, z ,t, y, g_true = data_simulator.demand(n, ypcor=0.5)

print("Data shapes:\n\
        Features:{x} \n\
        Instruments: {z} \n\
        Treatment: {t} \n\
        Response: {y}".format(**{'x':x.shape, 'z':z.shape,
                                 't':t.shape, 'y':y.shape}))
