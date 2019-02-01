function handleMenu() {
  /**
   * This function toggles the hamburger menu open/close
   * Toggles class .mobile-links_open
   **/
  document.querySelector('.hamburger-menu').addEventListener('click', function() {
    document.querySelector('.hamburger-menu').classList.toggle('mobile-links_open');
    document.querySelector('.mobile-links').classList.toggle('mobile-links_open');
    console.log('toggle menu');
  });
}

const Slider = (function() {
  const onboardingSlider = document.getElementById('onboarding');
  const landingPage = document.getElementById('landing-page-body');
  const toggleSliderBtns = document.querySelectorAll('.toggle-slider');
  let onboarding;

  if (onboardingSlider) { onboardingSlider.style.display = 'none'; }


  function addListeners() {
    toggleSliderBtns.forEach(function(slider) {
      slider.addEventListener('click', toggleSlider)
    });
    document.getElementById('learn-1').addEventListener('click', function() {
      goToSlide(0);
    });
    document.getElementById('learn-2').addEventListener('click', function() {
      goToSlide(1);
    });
    document.getElementById('learn-3').addEventListener('click', function() {
      goToSlide(2);
    });
  }

  function initSlider() {
    /**
      * Options for the onboarding slider
    **/
    onboarding = tns({
      container: '.my-slider',
      items: 1,
      mouseDrag: true,
      controls: false,
      navPosition: 'bottom',
    });
  }

  function toggleSlider() {
    if (onboardingSlider.style.display === 'none') {
      show(onboardingSlider);
      hide(landingPage);
    } else {
      show(landingPage);
      hide(onboardingSlider);
    }
  }

  function hide(el) {
    el.style.display = 'none';
  }

  function show(el) {
    el.style.display = 'block';
  }

  function goToSlide(number) {
    landingPage.style.display = 'none';
    onboardingSlider.style.display = 'block';
    onboarding.goTo(number);
  }

  return {
    init: function() {
      initSlider();
      addListeners();
    }
  }

})();

(function() {
  /**
    * Runs on load and calls functions that's needed for landing page
    * handleMenu -> creates mobile menu that can toggle
    * AOS -> scroll reveal elements
    * Slider -> options for onboarding slider
  **/
  handleMenu();
  AOS.init();
  Slider.init();
})();