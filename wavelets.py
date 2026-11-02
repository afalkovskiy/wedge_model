import streamlit as st
from streamlit.components.v1 import html

st.title('Wavelets with Wedge Model')
st.subheader('Alex Falkovskiy')
url = "https://www.rmseismic.com"

st.write('This web app is a tool which helps to visualise how wedge model would look like on a seismic section.')
st.write('It convolves selected wavelet with reflectivity series and calculates a synthetic traces for a wedge model.')
st.write('You can select wavelet and vary model parameters and see how your seismic section would change on the fly.')

st.write('Here is the list of wavelets you can display to calculate a synthetic trace:')
st.write('**Ricker, Ormsby, Klauder**. Use a left side menu to select a wavelet and sliders to change parameters.')
st.write('Wavelet equations are from a paper by Harold Ryan: Ricker, Ormsby; Klauder, Butterworth - A Choice of wavelets, publised in CSEG Recorder, September 1994.')
st.write('This is another classical work which provides math foundation for the wedge model:  \nWidess, M. B., 1973, How thin is a thin bed?: Geophysics, 38, 1176-1180.')

url1 = "https://www.rmseismic.com/lasviewer.html"

st.write("A.F., August 2026")
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
 
