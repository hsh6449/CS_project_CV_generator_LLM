window.addEventListener("DOMContentLoaded", (event) => {
	const sidebarWrapper = document.getElementById("sidebar-wrapper");
	const scrollToTop = document.querySelector(".scroll-to-top");

	if (!sidebarWrapper) {
		console.error("Sidebar wrapper not found!");
	} else {
		let scrollToTopVisible = false;

		// Closes the sidebar menu
		const menuToggle = document.body.querySelector(".menu-toggle");
		if (menuToggle) {
			menuToggle.addEventListener("click", (event) => {
				event.preventDefault();
				sidebarWrapper.classList.toggle("active");
				_toggleMenuIcon();
				menuToggle.classList.toggle("active");
			});
		} else {
			console.error("Menu toggle button not found!");
		}

		// Closes responsive menu when a scroll trigger link is clicked
		const scrollTriggerList = [].slice.call(
			document.querySelectorAll("#sidebar-wrapper .js-scroll-trigger")
		);
		scrollTriggerList.forEach((scrollTrigger) => {
			scrollTrigger.addEventListener("click", () => {
				sidebarWrapper.classList.remove("active");
				if (menuToggle) {
					menuToggle.classList.remove("active");
				}
				_toggleMenuIcon();
			});
		});

		function _toggleMenuIcon() {
			const menuToggleBars = document.body.querySelector(
				".menu-toggle > .fa-bars"
			);
			const menuToggleTimes = document.body.querySelector(
				".menu-toggle > .fa-xmark"
			);
			if (menuToggleBars) {
				menuToggleBars.classList.remove("fa-bars");
				menuToggleBars.classList.add("fa-xmark");
			}
			if (menuToggleTimes) {
				menuToggleTimes.classList.remove("fa-xmark");
				menuToggleTimes.classList.add("fa-bars");
			}
		}

		// Scroll to top button appear
		document.addEventListener("scroll", () => {
			if (!scrollToTop) {
				console.error("Scroll to top button not found!");
				return;
			}
			if (document.documentElement.scrollTop > 100) {
				if (!scrollToTopVisible) {
					fadeIn(scrollToTop);
					scrollToTopVisible = true;
				}
			} else {
				if (scrollToTopVisible) {
					fadeOut(scrollToTop);
					scrollToTopVisible = false;
				}
			}
		});

		// Scroll to top button functionality
		if (scrollToTop) {
			scrollToTop.addEventListener("click", (event) => {
				event.preventDefault();
				window.scrollTo({ top: 0, behavior: "smooth" });
			});
		}
	}
});

function fadeOut(el) {
	el.style.opacity = 1;
	(function fade() {
		if ((el.style.opacity -= 0.1) < 0) {
			el.style.display = "none";
		} else {
			requestAnimationFrame(fade);
		}
	})();
}

function fadeIn(el, display) {
	el.style.opacity = 0;
	el.style.display = display || "block";
	(function fade() {
		var val = parseFloat(el.style.opacity);
		if (!((val += 0.1) > 1)) {
			el.style.opacity = val;
			requestAnimationFrame(fade);
		}
	})();
}

function _toggleMenuIcon() {
	const menuToggleBars = document.body.querySelector(".menu-toggle > .fa-bars");
	const menuToggleTimes = document.body.querySelector(
		".menu-toggle > .fa-xmark"
	);
	if (menuToggleBars) {
		menuToggleBars.classList.remove("fa-bars");
		menuToggleBars.classList.add("fa-xmark");
	}
	if (menuToggleTimes) {
		menuToggleTimes.classList.remove("fa-xmark");
		menuToggleTimes.classList.add("fa-bars");
	}
}
