pip install .
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"emiliocapitaine96@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
base=\"dark\"\n\
primaryColor=\"#7c20a2\"\n\
" > ~/.streamlit/config.toml
