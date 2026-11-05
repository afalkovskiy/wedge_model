import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import math
# import plotly.graph_objects as go
# import time

st.set_page_config(layout="wide")


if "f" not in st.session_state:
    st.session_state["f"] = 25.
f = st.session_state["f"]  

if "phi" not in st.session_state:
    st.session_state["phi"] = 0.
phi = st.session_state["phi"]  

pi = math.pi
nTraces = 20
nLayers = 6
nLayersMax = 6
length1 = 0.6
dt1=0.001

trace_arr = []
refl_arr = []
layers_arr = []                 # each element is layer_y with y coordinates of one layer (2way time)

layer_x = np.arange(nTraces)    # x coordinates for plotting layers, the same for all layers
layer_y = np.zeros(nTraces)     # y coordinates of layar for plotting (2way time)
layer_y_d = np.zeros(nTraces)   # y coordinates of layar for plotting (depth (m))

if 'w_arr' not in st.session_state: 
    # st.session_state.w_arr = [300.] * (nLayers + 1)   # each layer thickness
    st.session_state.w_arr =[100.0, 300.0, 100.0, 400.0, 300.0, 300.0, 300.0]

if 'd_arr' not in st.session_state: 
    st.session_state.d_arr = [0.] * (nLayers + 1)   # depth of i-th layer bottom

if 't_arr' not in st.session_state: 
    st.session_state.t_arr = [0.] * (nLayers + 1)   # 2-way time to i-th layer bottom   

if 'ri_arr' not in st.session_state: 
    st.session_state.ri_arr = [-0.11, -0.22, 0.38, -0.30, 0.32, 0.]  # ri_arr[i] = reflextivity between i-th and (i+1)-th layers

print('w_arr:', st.session_state.w_arr)    
print('d_arr:', st.session_state.d_arr)

if 'lith_arr' not in st.session_state:
    st.session_state.lith_arr = [None] * (nLayers + 1)    # array with litholory objects for each layer

if 'lith_ind_arr' not in st.session_state:
    st.session_state.lith_ind_arr = [0, 1, 2, 3, 4, 5, 6]   # array with litholory indices for each layer


# width_arr = [0.] * nLayers      # thickness of each layer
options1 = ["Limestone", "Sandstone", "Shale", "Dolomite", "Salt", "Basement"]

# lithology dictionaries for different rock types
shale = {'name':'Shale', 'rho':2.3, 'v':3.6, 'color':'#bebebe', 'hatch':'--'}
sandstone = {'name':'Sandstone', 'rho':2.6, 'v':5.0, 'color':'#ffff00', "hatch": "o"}
# sandstone = {'name':'Sandstone', 'rho':2.6, 'v':5.0, 'color':'green', "hatch": ".."}
limestone = {'name': 'Limestone', 'rho':2.7, 'v':6.0, 'color':'#3891f0', "hatch": "+"}
dolomite = {'name': 'Dolomite', 'rho':2.75, 'v':6.7, 'color':'#8080ff', "hatch": "-/"}
salt = {'name': 'Salt', 'rho':2.2, 'v':4.5, 'color':'#7ddfbe', "hatch": "++"}
basement = {'name': 'Basement', 'rho':2.8, 'v':6.8, 'color':'#ef138a', "hatch": "-|"}

all_lith = [shale, limestone, sandstone, shale, dolomite, salt, basement]
st.session_state.lith_arr = [shale, limestone, sandstone, shale, dolomite, sandstone, basement]  # initial model

# st.title("Ricker wavelet: Wedge model 2")

def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))
    y = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    return t, y

def ORMSBY(f1=5., f2=10., f3=40., f4=45., length=0.512, dt=0.001):
    p = np.pi
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))

    y = p*f4**2 * (np.sinc(f4*t))**2/(f4-f3) - p*f3**2 * (np.sinc(f3*t))**2/(f4-f3) - \
        p*f2**2 * (np.sinc(f2*t))**2/(f2-f1) +  p*f1**2 * (np.sinc(f1*t))**2/(f2-f1)

    y = y / np.amax(abs(y))

    return t, y

def Klauder(T=6., f1=10., f2=40., length=0.512, dt=0.001):
    k = (f2 - f1)/T
    f0 = (f2 + f1)/2
    i = complex(0, 1)
    p = np.pi
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))
    #y = t**2

    a = np.exp(2*pi*i*f0*t)
    y = (a * np.sin(pi*k*t*(T - t)) / (pi*k*t)).real

    return t, y

col100, col200, col202, col300 = st.columns([3, 6, 3.5, 5.5])

with col100:
    st.subheader('Model parameters')

    layer = st.selectbox("Layer number", options=range(1, nLayers+1), label_visibility="visible")
    # nLayersMax = max(nLayersMax, layer)
    nLayersMax = nLayers

    lith_indx = st.session_state.lith_ind_arr[layer]
    lith1 = st.selectbox("Select lithology", options1, index=lith_indx-1, label_visibility="visible")


    indx_lith1 = options1.index(lith1)
    v1 = all_lith[indx_lith1]['v']
    rho1 = all_lith[indx_lith1]['rho']

    st.session_state.lith_arr[layer] = all_lith[indx_lith1]
    st.session_state.lith_ind_arr[layer] = indx_lith1 + 1

    print('lith_ind_arr', st.session_state.lith_ind_arr)

    # thickness = st.slider('Layer thickness (m)', min_value=10., max_value=400., value=300., step=5., format="%.1f") 
    w1 = st.session_state.w_arr[layer-1]
    thickness = st.slider('Layer thickness (m)', min_value=10., max_value=400., value=w1, step=5., format="%.1f") 
    
    st.session_state.w_arr[layer-1] = thickness
    st.markdown(f"Layer {layer}: {lith1} {thickness} m, v={v1} km/s, {rho1} g/cc")
    # formatted_items = [f"{val:.2f}" for val in st.session_state.ri_arr]
    formatted = "Reflectivity Ri: "
    # for val in st.session_state.ri_arr:
    #     formatted = formatted + f" {val:.2f}"

    for i in  range(nLayers - 1):      
        formatted = formatted + f" {st.session_state.ri_arr[i]:.2f}"

    st.markdown(f"{formatted}")

    # filling depth and 2-way time arrays
    for i in range(nLayers + 1):
        try:
            lith_indx = st.session_state.lith_ind_arr[i+1]
            v1 = all_lith[lith_indx]['v']
        except:
            v1 = 10000000.           
        if i==0:
           st.session_state.d_arr[i] = 0
           st.session_state.t_arr[i] = 2.* st.session_state.w_arr[i] / v1
        else:          
            st.session_state.d_arr[i] = st.session_state.d_arr[i-1] + st.session_state.w_arr[i-1]
            st.session_state.t_arr[i] = st.session_state.t_arr[i-1] + 2.* st.session_state.w_arr[i] / v1

    # print('*** w_arr:', st.session_state.w_arr)    
    # print('*** d_arr:', st.session_state.d_arr)
    # print('*** t_arr:', st.session_state.t_arr)

dr = 0.1        #refl. interval
wedge_shift = 3 #wedge_shift ms per trace


with col200:
    st.subheader('Model')

    # wedge model in depth
    fig0 = plt.figure(figsize=(4,2.3))
    plt.subplot(111)
    for i in range(nLayersMax):

        try:
            lith_indx = st.session_state.lith_ind_arr[i+1]
            c1 = all_lith[lith_indx]['color']  
            h1 = all_lith[lith_indx]['hatch']   
            l1 = all_lith[lith_indx]['name']  
        except:
            c1 = 'black'
            h1 = ' '
            l1 = ''      

        if i < 3:
            layer_y_d1 = np.ones(nTraces)*st.session_state.d_arr[i]
            layer_y_d2 = np.ones(nTraces)*st.session_state.d_arr[i+1]

        if i==3:
            incr = st.session_state.w_arr[i]/(nTraces - 1.)
            for j in range(nTraces): 
                layer_y_d1 = np.ones(nTraces)*st.session_state.d_arr[i]             
                layer_y_d2[j] = layer_y_d1[j] + incr*j

        if i>3:
            layer_y_d1 = layer_y_d2.copy()
            for j in range(nTraces):
                layer_y_d2[j] = layer_y_d1[j] + st.session_state.w_arr[i]


        # plt.fill_between(layer_x, st.session_state.d_arr[i], st.session_state.d_arr[i+1], color=c1, alpha=0.15, label=l1)
        #   
        plt.fill_between(layer_x, layer_y_d1, layer_y_d2, hatch=h1, alpha=0.15)
        plt.fill_between(layer_x, layer_y_d1, layer_y_d2, color=c1, alpha=0.15, label=l1)
   



    # plt.legend()
    plt.legend(fontsize=5, loc='upper right', bbox_to_anchor=(0.95, 0.95))


    plt.gca().invert_yaxis()
    # plt.xlabel("Reflectivity")
    plt.ylabel("Depth (m)")
    st.pyplot(fig0)

with col202:
    str1 = "Wavelet parameters"
    st.subheader(f"**{str1}**")
    # st.latex(r'''
    # A(t) = (1-2\pi^2 f^2 t^2)e^{-\pi^2 f^2 t^2}
    # ''') 
    # st.latex(r'''
    # A(t)=\frac{\pi f_4^2 sinc^2 (\pi f_4 t) - \pi f_3^2 sinc^2 (\pi f_3 t)}{f_4 - f_3} \\
    # - \frac{\pi f_2^2 sinc^2 (\pi f_2 t) - \pi f_1^2 sinc^2 (\pi f_1 t)}{f_2 - f_1}
    # ''') 

    st.latex(r'''
    A(t) = Re (\frac{sin(\pi kt(T-t))}{\pi kt} e^ {2 \pi if_0 t}), \\
    where \; k = \frac{f_2 - f_l}{T}, fo = \frac{f_2 + f_l}{2}, i = \sqrt{-1}
    ''')
    

    st.slider('Wavelet phase rotation (deg)', key="phi", min_value=0., max_value=360., step=45., format="%.1f") 

    # if "f" not in st.session_state:
    #     st.session_state["f"] = 25.
    # f = st.session_state["f"]  

    # if "phi" not in st.session_state:
    #     st.session_state["phi"] = 0.
    # phi = st.session_state["phi"]  


    # if "f12" not in st.session_state:
    #     st.session_state["f12"] = (5., 10.)
    # f1, f2 = st.session_state["f12"]  

    # if "f34" not in st.session_state:
    #     st.session_state["f34"] = (60., 70.)
    # f3, f4 = st.session_state["f34"] 

    
    # st.slider(' f1 - f2 (Hz)', key="f12", min_value=1., max_value=120., step=1., format="%.1f")
    # st.slider(' f3 - f4 (Hz)', key="f34", min_value=f2, max_value=120., step=1., format="%.1f")
    
    # envelope = st.checkbox('Envelope')


    if "f" not in st.session_state:
        st.session_state["f"] = 25.
    f = st.session_state["f"]  

    if "phi" not in st.session_state:
        st.session_state["phi"] = 0.
    phi = st.session_state["phi"]  


    if "f12" not in st.session_state:
        st.session_state["f12"] = (10., 40.)
    f1, f2 = st.session_state["f12"]  

    # if "f34" not in st.session_state:
    #     st.session_state["f34"] = (60., 70.)
    # f3, f4 = st.session_state["f34"] 

    if "T" not in st.session_state:
        st.session_state["T"] = 7.
    T = st.session_state["T"]  

    st.slider('Low and high terminal frequency (Hz)', key="f12", min_value=1., max_value=240., step=1., format="%.1f")
        # st.slider(' f3 - f4 (Hz)', key="f34", min_value=f2, max_value=120., step=1., format="%.1f")
    st.slider('Duration of input signal (s)', key="T", min_value=5., max_value=10., step=1., format="%.1f")
    

   
if "scl" not in st.session_state:
    st.session_state["scl"] = 1.3 
          
scl = st.session_state["scl"]

# str1 = "Ricker " + str(int(f + 0.5)) + " Hz, φ = " + str(int(phi+0.5)) + "°"
# str1 = "Ormsby " + str(int(f1 + 0.5)) + " - " + str(int(f2 + 0.5))  + " - " + str(int(f3 + 0.5)) + " - " + str(int(f4 + 0.5)) + " Hz, Phase " + str(int(phi+0.5)) + "°"
str1 = "Klauder " + str(int(f1 + 0.5)) + " - " + str(int(f2 + 0.5))  + " Hz, " + str(int(T + 0.5))   + " sec, Phase " + str(int(phi+0.5)) + "°"


col2, col3 = st.columns(2)              #?????? to check usage

# t, y = ricker (f)
# t, y = ORMSBY(f1, f2, f3, f4, 0.512, 0.001)
t, y = Klauder(T, f1, f2, 0.512, 0.001)

z= hilbert(y) #form the analytical signal
inst_amplitude = np.abs(z) #envelope extraction
inst_phase = np.unwrap(np.angle(z))#inst phase
    
phase = phi * pi/180
x_rotate = math.cos(phase)*z.real - math.sin(phase)*z.imag

# fig = go.Figure()
# fig0 = plt.figure(figsize=(4,2.4), alpha=.45)
fig0 = plt.figure(figsize=(4,2.3))

with col300:    #plot wavelet

    # str1 = "Ricker " + str(int(f + 0.5)) + " Hz, φ = " + str(int(phi+0.5)) + "°"
    st.subheader(f"**{str1}**")
    envelope = st.checkbox('Envelope')
    # st.title(f"**{str1}**")

    if envelope:
        chart_data = pd.DataFrame(
           {
               "t": t,
               #"y": y
               "y": x_rotate,
               "y_env2": inst_amplitude,
               "y_env3": -1*inst_amplitude
           }
        )
        # st.line_chart(chart_data, x="t", y=["y", "y_env2", "y_env3"], color=["#d62728", "#D3D3D3", "#D3D3D3"], width=450, height=450)

        plt.plot(chart_data['t'], chart_data['y'], color='tab:red', alpha=.45)
        plt.plot(chart_data['t'], chart_data['y_env2'], color='tab:grey', alpha=.45)
        plt.plot(chart_data['t'], chart_data['y_env3'], color='tab:grey', alpha=.45)      
    
    else:
        chart_data = pd.DataFrame(
           {
               "t": t,
               "y": x_rotate
           }
        )

        plt.plot(chart_data['t'], chart_data['y'], color='tab:red', alpha=.45)
    plt.grid()
    st.pyplot(fig0) 



# length1 = 0.6
# dt1=0.001
x1 = np.linspace(0, length1, int(length1/dt1))
y1 = 0.* x1
 
ns = int(dr/dt1)
wedge_samples = int(wedge_shift/(dt1*1000.))

# nLayers = int(length1/dr)
nLayers = min(int(length1/dr), nLayers)

for i in range(nLayers + 1):
    layer_y = np.zeros(nTraces) # 2-way time boundary
    layers_arr.append(layer_y)

for j in range(nTraces):
    y1 = 0.* x1
 
    ns = int(dr/dt1)
    # st.write('dr =', dr, ' dt = ', dt1, ' ns = ', ns)
    # y1[ns] = -1.
    for i in range(nLayers+1):
   
        try:
            lith_indx1 = st.session_state.lith_ind_arr[i+1]
            lith_indx2 = st.session_state.lith_ind_arr[i+2]
            # print("lith_indrx1 = ", lith_indx1, "lith_indrx2 = ", lith_indx2)
            rho1 = all_lith[lith_indx1]['rho'] 
            rho2 = all_lith[lith_indx2]['rho'] 
            # print("rho1 = ", rho1, "rho2 = ", rho2)

            v1 = all_lith[lith_indx1]['v'] 
            v2 = all_lith[lith_indx2]['v'] 
            rf=(rho2*v2 - rho1*v1)/(rho2*v2 + rho1*v1)

            # rf = -1.
        except:
            rf = 0. 



        ni = int(st.session_state.t_arr[i]/(dt1*1000.))      # sample number at this travel time

        # y1[ni] = rf

        if i<3:
            layers_arr[i][j] = ni*1.
            ni2 = ni
            # y1[ni] = rf
        if i==3:
            ni = int(st.session_state.t_arr[i-1]/(dt1*1000.))    
            incr = (st.session_state.t_arr[i] - st.session_state.t_arr[i-1])/(dt1*1000.*((nTraces-1.)))
            layers_arr[i][j] = ni*1. + incr*j
            ni2 = int(ni + incr*j)
            # y1[int(ni + incr*j)] = rf

        if i>3:
            ni = int(st.session_state.t_arr[i-1]/(dt1*1000.))    
            incr = (st.session_state.t_arr[i] - st.session_state.t_arr[i-1])/(dt1*1000.*((nTraces-1.)))
            dt = st.session_state.t_arr[i] - st.session_state.t_arr[i-1]
            # layers_arr[i][j] = ni*1. + incr*j
            layers_arr[i][j] = layers_arr[i-1][j]  + dt
            # ni2 = int(ni + incr*j)  
            ni2 = int(layers_arr[i][j]/(dt1*1000.))   




        if ni2 > len(y1) - 1:
            ni2 = len(y1) -1
            rf = 0.
  
        y1[ni2] = rf

        if j==0:
            st.session_state.ri_arr[i] = rf
        


    refl_arr.append(y1)
    y2 = scl*np.convolve(refl_arr[j], x_rotate, mode='same')


    trace_arr.append(y2)
# reflectivity plot
fig1 = plt.figure(figsize=(4,2.3))



for i in range(nTraces):
    plt.plot(refl_arr[i] + i, 1000*x1, color='tab:red', linewidth=0.75)

for i in range(nLayers+1):

    try: 
        lith_indx = st.session_state.lith_ind_arr[i+1]
        c1 = all_lith[lith_indx]['color']  
        h1 = all_lith[lith_indx]['hatch']   
        l1 = all_lith[lith_indx]['name']  
    except:
        c1 = 'black'
        h1 = ' '
        l1 = ''      

    if i==0:
        # plt.fill_between(layer_x, 0*layers_arr[i], layers_arr[i], hatch=h1, alpha=0.1)
        plt.fill_between(layer_x, 0*layers_arr[i], layers_arr[i], facecolor=c1, edgecolor='grey', hatch=h1, alpha=0.15, label=l1)  
    else:           
        # plt.fill_between(layer_x, layers_arr[i-1], layers_arr[i], hatch=h1, alpha=0.1)
        plt.fill_between(layer_x, layers_arr[i-1], layers_arr[i], facecolor=c1, edgecolor='grey', hatch=h1, alpha=0.15, label=l1)




# plt.legend()
plt.legend(fontsize=5, loc='upper right', bbox_to_anchor=(0.95, 0.95))


plt.gca().invert_yaxis()
# plt.xlabel("Reflectivity")

plt.ylabel("Two-way time (ms)")

# trace display
fig2 = plt.figure(figsize=(4,2.3), alpha=.45)
# fig2.suptitle('Convolved')
# plt.xlabel("Trace #")
plt.ylabel("Two-way time (ms)")

# plt.subplot(111)

# plot traces
for i in range(nTraces):
    # plt.plot(trace_arr[i] + i, 1000*x1, color='tab:blue', alpha=.45, linewidth=0.75)
    plt.plot(trace_arr[i] + i, 1000*x1, color='tab:blue', linewidth=0.75)
    y2pos = np.maximum(0,trace_arr[i])
    plt.fill_betweenx(1000*x1, y2pos + i, i,  color='tab:blue', alpha=.85)


# plot lithology
for i in range(nLayersMax):

    try: 
        lith_indx = st.session_state.lith_ind_arr[i+1]
        c1 = all_lith[lith_indx]['color']  
        h1 = all_lith[lith_indx]['hatch']   
        l1 = all_lith[lith_indx]['name']  
    except:
        c1 = 'black'
        h1 = ' '
        l1 = '' 

    if i==0:
        # plt.fill_between(layer_x, 0*layers_arr[i], layers_arr[i], hatch=h1, alpha=0.08)
        # plt.fill_between(layer_x, 0*layers_arr[i], layers_arr[i], color=c1, alpha=0.08, label=l1) 
        plt.fill_between(layer_x, 0*layers_arr[i], layers_arr[i], facecolor=c1, edgecolor='grey', hatch=h1, alpha=0.15, label=l1)  
    else:           
        # plt.fill_between(layer_x, layers_arr[i-1], layers_arr[i], hatch=h1, alpha=0.08)
        # plt.fill_between(layer_x, layers_arr[i-1], layers_arr[i], color=c1, alpha=0.08, label=l1)
        plt.fill_between(layer_x, layers_arr[i-1], layers_arr[i], facecolor=c1, edgecolor='grey', hatch=h1, alpha=0.15, label=l1)


plt.legend(fontsize=5, loc='upper right', bbox_to_anchor=(0.95, 0.95))
plt.gca().invert_yaxis()

with col2:
    st.subheader('Reflectivity')

    st.pyplot(fig1) 

with col3:
    st.subheader('Synthetic seismic')
    st.pyplot(fig2)
    st.slider('Trace scalar', key="scl", min_value=0.2, max_value=10., step=0.1, format="%.1f")


    # st.markdown("<br>", unsafe_allow_html=True)
    url1 = "https://www.rmseismic.com/lasviewer.html"
    st.write("More geophysical apps: [rmseismic.com](%s)" % url1)


# print(st.session_state.lith_arr) 
# st.write(st.session_state.lith_arr)   