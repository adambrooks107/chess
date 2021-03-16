from cairosvg import svg2png

## handle = rsvg.Handle(<svg filename>)
# or, for in memory SVG data:
svg_code = """<svg height="90" version="1.1" viewBox="0 0 45 45" width="90"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"><g class="black king" fill="none" fill-rule="evenodd" id="black-king" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5">
            <path d="M22.5 11.63V6" stroke-linejoin="miter" />
            <path d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5" fill="#000" stroke-linecap="butt" stroke-linejoin="miter" />
            <path d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z" fill="#000" />
            <path d="M20 8h5" stroke-linejoin="miter" />
            <path d="M32 29.5s8.5-4 6.03-9.65C34.15 14 25 18 22.5 24.5l.01 2.1-.01-2.1C20 18 9.906 14 6.997 19.85c-2.497 5.65 4.853 9 4.853 9M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0" stroke="#fff" />
        </g></svg>"""

svg2png(bytestring=svg_code,write_to='assets/black_king.png')