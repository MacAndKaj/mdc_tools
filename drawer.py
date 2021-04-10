import matplotlib.pyplot as plt

u_filename = 'u_ident.txt'
y_filename = 'y_ident.txt'

u_file = open("files/" + u_filename, 'r')
y_file = open("files/" + y_filename, 'r')
u_map = {}
for l in u_file:
    l_s = l.split('|')
    u_map[int(l_s[0])] = float(l_s[1])

u_file.close()
y_map = {}
for l in y_file:
    l_s = l.split('|')
    y_map[int(l_s[0])] = float(l_s[1])

y_file.close()

fig, axs = plt.subplots(2)

axs[0].plot(list(y_map.keys())[500:800], list(y_map.values())[500:800])
axs[0].grid(True)
axs[1].plot(list(u_map.keys())[500:800], list(u_map.values())[500:800])
plt.show()
