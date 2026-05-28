import os
import streamlit as st
import streamlit.components.v1 as components
import base64
 

def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def inject_local_font(font_path, font_name):
    if not os.path.exists(font_path):
        return
    
    with open(font_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    ext = os.path.splitext(font_path)[1].lstrip(".")
    fmt = {"otf": "opentype"}.get(ext, ext)
    mime = {"otf": "font/otf"}.get(ext, f"font/{ext}")

    st.markdown(f"""
        <style>
        @font-face {{
            font-family: '{font_name}';
            src: url('data:{mime};base64,{encoded}') format('{fmt}');
            font-weight: 100 900;
            font-style: normal;
        }}
        </style>
    """, unsafe_allow_html=True)

def inject_webrtc_styles():
    font_path = os.path.join(os.getcwd(), "static", "AdobeClean.otf")
    
    if not os.path.exists(font_path):
        return

    with open(font_path, "rb") as font_file:
        encoded_font = base64.b64encode(font_file.read()).decode()

    components.html(
        f"""
        <script>
        (function patchWebRTCStyles() {{
            function injectIntoIframe(iframe) {{
                try {{
                    const doc = iframe.contentDocument || iframe.contentWindow.document;
                    if (!doc || !doc.head) return;
                    if (doc.head.querySelector('#webrtc-custom-styles')) return;
                    const style = doc.createElement('style');
                    style.id = 'webrtc-custom-styles';
                    style.textContent = `
                        @font-face {{
                            font-family: 'AdobeClean';
                            src: url('data:font/otf;base64,{encoded_font}') format('opentype');
                            font-weight: 100 900;
                            font-style: normal;
                        }}
                        .MuiButtonBase-root,
                        .MuiButton-root,
                        .MuiButton-contained,
                        .MuiButton-text {{
                            border-radius: 0 !important;
                            font-family: 'AdobeClean', sans-serif !important;
                            letter-spacing: 0.05em !important;
                        }}
                    `;
                    doc.head.appendChild(style);
                }} catch (e) {{
                    console.warn('[patcher] could not inject:', e);
                }}
            }}

            function findAndPatch() {{
                const parentDoc = window.parent.document;
                const iframes = parentDoc.querySelectorAll('iframe');
                iframes.forEach(iframe => {{
                    if (iframe.src && iframe.src.includes('webrtc')) {{
                        if (iframe.contentDocument && iframe.contentDocument.readyState === 'complete') {{
                            injectIntoIframe(iframe);
                        }} else {{
                            iframe.addEventListener('load', () => injectIntoIframe(iframe));
                        }}
                    }}
                }});
            }}

            findAndPatch();
        }})();
        </script>
        """,
        height=0,
    )


def inject_strong_input_overrides():
    """Inject JS that force-applies dark theme styles to inputs, selects,
    and textareas, running on DOM mutations and periodically to override
    browser autofill and Streamlit runtime styles."""
    components.html(
        """
        <script>
        (function() {
            const STYLE_ID = 'strong-theme-overrides';
            if (document.getElementById(STYLE_ID)) return;

            const css = `
            input, textarea, select, .stSelectbox, .stTextInput {
                background-color: #0A0D14 !important;
                color: #ffffff !important;
                border: 1px solid rgba(255,255,255,0.06) !important;
            }
            input::placeholder, textarea::placeholder { color: rgba(255,255,255,0.6) !important; }
            `;

            const style = document.createElement('style');
            style.id = STYLE_ID;
            style.appendChild(document.createTextNode(css));
            document.head.appendChild(style);

            function applyInline(el) {
                try {
                    if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT')) {
                        el.style.backgroundColor = '#0A0D14';
                        el.style.color = '#ffffff';
                        el.style.border = '1px solid rgba(255,255,255,0.06)';
                    }
                } catch(e) {}
            }

            function applyAll() {
                document.querySelectorAll('input, textarea, select').forEach(applyInline);
                // also target common Streamlit wrapper nodes
                document.querySelectorAll('[data-testid="stSelectbox"] div, [data-testid="stTextInput"] input').forEach(el => el && (el.style.backgroundColor = '#0A0D14'));
            }

            // Run periodically (covers autofill and late-rendered widgets)
            applyAll();
            const interval = setInterval(applyAll, 600);

            // Observe DOM changes
            const mo = new MutationObserver(mutations => {
                for (const m of mutations) {
                    if (m.addedNodes && m.addedNodes.length) {
                        m.addedNodes.forEach(node => {
                            if (node.querySelectorAll) node.querySelectorAll('input,textarea,select').forEach(applyInline);
                            applyInline(node);
                        });
                    }
                }
            });
            mo.observe(document.body, { childList: true, subtree: true });
        })();
        </script>
        """,
        height=0,
    )
