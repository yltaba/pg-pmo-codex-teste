function scrollToAnchorWhenReady() {
    if (window.location.hash) {
        var anchor = window.location.hash.substring(1);

        function tryScroll() {
            var el = document.getElementById(anchor);
            if (el && (el.querySelector('svg, canvas'))) {
                el.scrollIntoView({behavior: "smooth", block: "center"});
                return true;
            }
            return false;
        }

        if (!tryScroll()) {
            // Observa o DOM até o gráfico aparecer e ser renderizado
            const observer = new MutationObserver(() => {
                if (tryScroll()) {
                    observer.disconnect();
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
        }
    }
}


window.addEventListener('hashchange', scrollToAnchorWhenReady);
window.addEventListener('popstate', scrollToAnchorWhenReady);
window.addEventListener('DOMContentLoaded', scrollToAnchorWhenReady);