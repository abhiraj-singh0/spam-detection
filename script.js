 document.addEventListener("DOMContentLoaded", function() {
        const menuBtn = document.getElementById('menuBtn');
        const navLinks = document.getElementById('navLinks');

        if (menuBtn && navLinks) {
            menuBtn.addEventListener('click', function(e) {
                e.preventDefault(); 
                
                // Toggles the menu sliding in
                navLinks.classList.toggle('active');
                
                // Toggles the hamburger turning into an 'X'
                menuBtn.classList.toggle('open'); 
            });

            // Closes the menu AND resets the 'X' back to a hamburger when a link is clicked
            const links = document.querySelectorAll('.nav-links li a');
            links.forEach(link => {
                link.addEventListener('click', () => {
                    navLinks.classList.remove('active');
                    menuBtn.classList.remove('open'); 
                });
            });
        }
    });