(() => {
  const nav = document.querySelector("[data-nav]");
  const toggle = document.querySelector(".nav__toggle");
  const mobileMenu = document.getElementById("nav-links");

  // Sticky nav state
  const onScroll = () => {
    if (window.scrollY > 32) nav.classList.add("is-scrolled");
    else nav.classList.remove("is-scrolled");
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile menu
  if (toggle && mobileMenu) {
    const isMobile = () => window.matchMedia("(max-width: 760px)").matches;
    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      mobileMenu.hidden = open ? false : isMobile();
    };
    // Initialize: hide on mobile
    if (isMobile()) mobileMenu.hidden = true;
    window.matchMedia("(max-width: 760px)").addEventListener("change", (e) => {
      if (!e.matches) mobileMenu.hidden = false;
      else if (toggle.getAttribute("aria-expanded") !== "true") mobileMenu.hidden = true;
    });
    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      setOpen(!expanded);
    });
    mobileMenu.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => setOpen(false));
    });
  }

  // Reveal on scroll
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduced && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-visible"));
  }
})();
