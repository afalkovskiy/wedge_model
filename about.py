import streamlit as st
from streamlit.components.v1 import html

st.title('Wavelets with Wedge Model')
st.subheader('Alex Falkovskiy')
url = "https://www.rmseismic.com"

st.write('This web app is a tool helping to visualise how wedge model would look like on a seismic section.')
st.write('It convolves selected wavelet with reflectivity series and calculates a synthetic traces for a wedge model.')
st.write('You can select wavelet and vary model parameters and see how your seismic section would change on the fly. ' \
'Use a left side menu to select a wavelet and sliders to change parameters.' \
'Select layer number and after that select lihology and thickness for this layer.')
st.write('A list of wavelets:')
st.write('**Ricker, Ormsby, Klauder**')
st.write('The following sources were used as a theoretical background of this application:')
st.write('Wavelet equations from a paper by Harold Ryan, 1994. Math foundation for using of the wedge model provided by Widess, M. B., 1973. ' \
'An overview of the techniques for prestack seismic amplitude analysis and examples of simple models from Bryan Russel, 1988.')

st.write('**References**')
st.write('Harold Ryan: Ricker, Ormsby; Klauder, Butterworth - A Choice of wavelets, publised in CSEG Recorder, September 1994.')
st.write('Widess, M. B., 1973, How thin is a thin bed?: Geophysics, 38, 1176-1180.')
st.write('Russell, B.H., 1988, Introduction to Seismic Inversion Methods.')


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
 
