"""
Minimal test to verify:
1. CSS background-image on .stApp via st.markdown works
2. st.components.v1.html() JS injection into parent document works
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Visual Test", layout="wide")

# TEST 1: Direct CSS on .stApp via st.markdown (style tags work, script tags don't)
st.markdown("""
<style>
.stApp {
    background-image: 
        linear-gradient(rgba(2,13,7,0.85), rgba(1,6,3,0.90)),
        url('https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=1920&q=80') !important;
    background-size: cover !important;
    background-position: center center !important;
    background-attachment: fixed !important;
}
</style>
""", unsafe_allow_html=True)

# TEST 2: Inject falling leaves via st.components.v1.html (JS actually executes here)
components.html("""
<script>
(function(){
    var doc = window.parent.document;
    if (!doc) { console.error('NO PARENT DOC'); return; }
    
    // Inject CSS for leaves
    if (!doc.getElementById('test-leaf-css')) {
        var style = doc.createElement('style');
        style.id = 'test-leaf-css';
        style.textContent = 
            '@keyframes leafFall { ' +
            '  0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; } ' +
            '  10% { opacity: 0.9; } ' +
            '  90% { opacity: 0.9; } ' +
            '  100% { transform: translateY(110vh) rotate(360deg); opacity: 0; } ' +
            '} ' +
            '#test-leaves { position:fixed; top:0; left:0; width:100vw; height:100vh; overflow:hidden; pointer-events:none; z-index:999999; } ' +
            '#test-leaves span { position:absolute; animation: leafFall linear infinite; pointer-events:none; }';
        doc.head.appendChild(style);
    }
    
    // Inject leaf container
    if (!doc.getElementById('test-leaves')) {
        var container = doc.createElement('div');
        container.id = 'test-leaves';
        var leafData = [
            {e:'🍃', l:'5%',  d:'18s', dl:'0s',  s:'36px'},
            {e:'🌿', l:'20%', d:'22s', dl:'3s',  s:'30px'},
            {e:'🌱', l:'35%', d:'20s', dl:'1s',  s:'40px'},
            {e:'🍀', l:'50%', d:'25s', dl:'5s',  s:'32px'},
            {e:'🍃', l:'65%', d:'19s', dl:'2s',  s:'38px'},
            {e:'🌿', l:'80%', d:'23s', dl:'4s',  s:'28px'},
            {e:'🌱', l:'90%', d:'21s', dl:'6s',  s:'34px'},
            {e:'🍀', l:'10%', d:'26s', dl:'7s',  s:'42px'},
            {e:'🍃', l:'45%', d:'17s', dl:'8s',  s:'36px'},
            {e:'🌿', l:'75%', d:'24s', dl:'3s',  s:'30px'}
        ];
        for (var i = 0; i < leafData.length; i++) {
            var span = doc.createElement('span');
            span.textContent = leafData[i].e;
            span.style.cssText = 'left:' + leafData[i].l + ';font-size:' + leafData[i].s + ';animation-duration:' + leafData[i].d + ';animation-delay:' + leafData[i].dl + ';';
            container.appendChild(span);
        }
        doc.body.appendChild(container);
        console.log('LEAVES INJECTED SUCCESSFULLY');
    }
})();
</script>
""", height=0, scrolling=False)

st.title("🌿 Visual Test Page")
st.write("If you can see a leafy background and falling leaf emojis, the approach works.")
st.write("If the background is plain dark, CSS on .stApp is being overridden.")
st.write("If no leaves are falling, st.components.v1.html JS injection is failing.")
