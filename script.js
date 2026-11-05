
document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons =
        document.querySelectorAll(".password-toggle");

    toggleButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const targetId = button.dataset.target;

            const passwordInput =
                document.getElementById(targetId);

            const icon = button.querySelector("i");

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                icon.classList.replace(
                    "bi-eye",
                    "bi-eye-slash"
                );

            } else {

                passwordInput.type = "password";

                icon.classList.replace(
                    "bi-eye-slash",
                    "bi-eye"
                );

            }

        });

    });


    // 2. Set minimum travel date

    const today = new Date();

    const localDate =
        new Date(
            today.getTime() -
            today.getTimezoneOffset() * 60000
        ).toISOString().split("T")[0];

    const dateInput =
        document.getElementById("homeTravelDate");

    if (dateInput) {
        dateInput.min = localDate;
    }
    const bookingForm =
        document.getElementById("bookingForm");

    if (bookingForm) {

        const travelDate =
            document.getElementById("id_travel_date");

        const travellers =
            document.getElementById("id_travellers");

        const budget =
            document.getElementById("id_budget");

        if (travelDate) {
            travelDate.min = localDate;
        }

        bookingForm.addEventListener(
            "submit",
            function (event) {

                if (
                    travelDate &&
                    travelDate.value < localDate
                ) {

                    alert("Please select a valid future travel date.");

                    event.preventDefault();

                    return;
                }

                if (
                    travellers &&
                    Number(travellers.value) < 1
                ) {

                    alert("At least one traveller is required.");

                    event.preventDefault();

                    return;
                }

                if (
                    budget &&
                    Number(budget.value) < 0
                ) {

                    alert("Budget cannot be negative.");

                    event.preventDefault();

                    return;
                }

            }
        );

    }
    const registerForm =
        document.getElementById("registerForm");

    if (registerForm) {

        registerForm.addEventListener(
            "submit",
            function (event) {

                const password =
                    document.getElementById("id_password1");

                const confirmPassword =
                    document.getElementById("id_password2");

                if (
                    password &&
                    confirmPassword &&
                    password.value !== confirmPassword.value
                ) {

                    alert("Passwords do not match.");

                    event.preventDefault();

                }

            }
        );

    }


    // 5. Smooth scrolling

    document.querySelectorAll(
        'a[href^="#"]'
    ).forEach(function (link) {

        link.addEventListener("click", function (event) {

            const target =
                document.querySelector(
                    link.getAttribute("href")
                );

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth"
                });

            }

        });

    });
});


document.addEventListener("DOMContentLoaded", function () {

    const destinationCards = document.querySelectorAll(".destination-card");

    destinationCards.forEach(function (card, index) {
        card.style.opacity = "0";

        card.style.animation = "destinationFadeIn 0.5s ease forwards";

        card.style.animationDelay = (index * 0.1) + "s";
    });

    const destinationImages = document.querySelectorAll(
        ".destination-image img, .destination-detail-image img"
    );

    destinationImages.forEach(function (image) {
        image.addEventListener("error", function () {
            this.style.display = "none";
            this.parentElement.style.background = "#dcebea";
        });
    });

    const exploreLink = document.querySelector(
        '.explore-hero-btn[href="#destination-list"]'
    );

    if (exploreLink) {
        exploreLink.addEventListener("click", function (event) {
            event.preventDefault();

            document.querySelector("#destination-list").scrollIntoView({
                behavior: "smooth"
            });
        });
    }

});

