function toggleMobileMenu(menu) {
  var container1 = document.querySelector('.container1');
  menu.classList.toggle('open');

  var mobileMenu = document.querySelector('.mobile-menu');

  if (menu.classList.contains('open')) {
    container1.style.marginTop = mobileMenu.offsetHeight + 'px';
  } else {
    container1.style.marginTop = '0';
  }
}

// Funkcja do sprawdzania rozmiaru ekranu i obsługi menu
function checkScreenSize(mobileMenu) {
  var mediaQuery = window.matchMedia('(min-width: 900px)');

  function handleScreenSizeChange(e) {
    if (e.matches) {
      // Jeśli szerokość ekranu jest większa niż 900px, zamknij menu
      mobileMenu.classList.remove('open');
      var container1 = document.querySelector('.container1');
      container1.style.marginTop = '0';
    }
  }

  // Wywołanie funkcji obsługującej zmiany rozmiaru ekranu
  mediaQuery.addListener(handleScreenSizeChange);

  // Uruchomienie funkcji, aby sprawdzić początkowy rozmiar ekranu
  handleScreenSizeChange(mediaQuery);
}

// Znajdź element menu mobilnego
var mobileMenu = document.querySelector('.mobile-menu');

// Wywołaj funkcję sprawdzającą rozmiar ekranu, gdy strona się załaduje
document.addEventListener('DOMContentLoaded', function() {
  checkScreenSize(mobileMenu);
});

