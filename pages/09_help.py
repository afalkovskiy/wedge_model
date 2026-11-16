import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

# Define your data
# data = {
#     'Lithology': ['Shale', 'Sandstone', 'Limestone', 'Dolomite', 'Salt', 'Basement'],
#     'Density (g/cc)': [2.3, 2.6, 2.7, 2.75, 2.2, 2.8],
#     'P-wave velocity (km/s)': [3.6, 2.6, 2.7, 2.75, 4.5, 2.8]
# }
# df = pd.DataFrame(data)

# lithology dictionaries for different rock types
shale = {'name':'Shale', 'rho':2.3, 'v':3.6, 'color':'#bebebe', 'hatch':'--'}
sandstone = {'name':'Sandstone', 'rho':2.6, 'v':5.0, 'color':'#ffff00', "hatch": "o"}
# sandstone = {'name':'Sandstone', 'rho':2.6, 'v':5.0, 'color':'green', "hatch": ".."}
limestone = {'name': 'Limestone', 'rho':2.7, 'v':6.0, 'color':'#3891f0', "hatch": "+"}
dolomite = {'name': 'Dolomite', 'rho':2.75, 'v':6.7, 'color':'#8080ff', "hatch": "-/"}
salt = {'name': 'Salt', 'rho':2.2, 'v':4.5, 'color':'#7ddfbe', "hatch": "++"}
basement = {'name': 'Basement', 'rho':2.8, 'v':6.8, 'color':'#ef138a', "hatch": "-|"}

all_lith = [shale, limestone, sandstone, dolomite, salt, basement]

columns = ['Lithology', 'Density (g/cc)', 'Vp (km/s)']

rows = []
for lith in all_lith:
    rows.append([lith['name'], lith['rho'], lith['v']])

df2 = pd.DataFrame(rows, columns=columns)


st.title('Wavelets with Wedge Model v.3')
url = "https://www.rmseismic.com"

st.write('This web app helps to visualise how a wedge model would look like on a seismic section.')
st.write('It uses a list of several lithology options with preselected typical velocity and density values to make creation of a model simple.')
st.write('Select lithology from this list and layer thickness from the Model parameters menu to to build a model.')

# Display a static table
st.subheader("Lithology parameters")
# st.table(df)

st.table(df2)

st.write('You can select wavelet and vary model parameters and see on the fly how your seismic section would change.')
st.write('Select layer number and after that select lihology and thickness for this layer.')
st.write('It convolves selected wavelet with reflectivity series and calculates a synthetic traces for a wedge model.')

st.write('A list of wavelets that can be used to calculate a synthetic trace:')
st.write('**Ricker, Ormsby, Klauder**. Use a left side menu to select a wavelet and sliders to change parameters.')
# st.write('Wavelet equations are from a paper by Harold Ryan: Ricker, Ormsby; Klauder, Butterworth - A Choice of wavelets, publised in CSEG Recorder, September 1994.')
# st.write('This is another classical work which provides math foundation for the wedge model:  \nWidess, M. B., 1973, How thin is a thin bed?: Geophysics, 38, 1176-1180.')

url1 = "https://www.rmseismic.com/lasviewer.html"

st.write("A.F., November 2026")
st.write("RM Seismic Software  \n [rmseismic.com](%s)" % url1)


google_js = """
<!-- Google tag (gtag.js) --><script async src="https://www.googletagmanager.com/gtag/js?id=G-VBX865DFKL"></script><script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-VBX865DFKL');
</script>
"""

#html1 = f"{google_js}"
 
