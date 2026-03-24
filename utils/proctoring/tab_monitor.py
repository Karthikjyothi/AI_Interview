import streamlit.components.v1 as components


def enforce_fullscreen():
    components.html(
        """
        <script>

        function enterFullscreen(){
            let elem = document.documentElement;

            if(elem.requestFullscreen){
                elem.requestFullscreen();
            }
        }

        // Listen for Streamlit button click
        window.addEventListener("click", function(){

            if(!document.fullscreenElement){
                enterFullscreen();
            }

        });

        // Detect exit fullscreen
        document.addEventListener("fullscreenchange", function(){

            if(!document.fullscreenElement){
                alert("⚠️ Fullscreen mode is required for this interview.");
            }

        });

        // Detect tab switching
        document.addEventListener("visibilitychange", function(){

            if(document.hidden){
                alert("⚠️ Tab switching detected!");
            }

        });

        // Detect window blur
        window.addEventListener("blur", function(){
            alert("⚠️ Window focus lost!");
        });

        </script>
        """,
        height=0,
    )