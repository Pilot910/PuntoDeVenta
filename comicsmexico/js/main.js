document.addEventListener("DOMContentLoaded", () => {
    const API_KEY = "123456";

    // Contenedores
    const newComicsRow = document.getElementById("new-comics");
    const coversModal = document.getElementById("covers-modal");
    const coversContainer = document.getElementById("covers-container");
    const modalTitle = document.getElementById("modal-title");
    const closeModalBtn = coversModal.querySelector(".close");

    // ===== Función para crear tarjeta de cómic =====
    function createComicHTML(comic) {
        const div = document.createElement("div");
        div.className = "comic";

        // Buscar portada regular activa
        const regularCover = comic.covers.find(c => c.ilustracion === "regular" && c.estado_activo == 1);

        // Convertir ruta a relativa dentro de comicsImg/
        let rutaRelativa = "img/logo.png"; // fallback
        if (regularCover && regularCover.ruta_imagen) {
            rutaRelativa = regularCover.ruta_imagen
                .replace(/\\/g, "/")
                .replace(/^C:\/xampp\/htdocs\/comicsmexico\//i, "")
                .replace(/^(?!comicsImg\/)/i, "comicsImg/");
        }

        div.innerHTML = `
            <img src="${rutaRelativa}" alt="${comic.titulo}">
            <h3>${comic.titulo}</h3>
        `;

        div.addEventListener("click", () => openCoversModal(comic));
        return div;
    }

    // ===== Modal de portadas =====
    async function openCoversModal(comic) {
        coversContainer.innerHTML = "";
        modalTitle.textContent = `Portadas de ${comic.titulo}`;

        try {
            const res = await fetch(`backend/get_covers.php?comic_id=${comic.id}&api_key=${API_KEY}`);
            const covers = await res.json();

            if (covers.error) {
                coversContainer.innerHTML = `<p>Error al cargar portadas: ${covers.error}</p>`;
                return;
            }

            covers.forEach(cover => {
                if (cover.estado_activo != 1) return;

                let rutaRelativa = cover.ruta_imagen
                    .replace(/\\/g, "/")
                    .replace(/^C:\/xampp\/htdocs\/comicsmexico\//i, "")
                    .replace(/^(?!comicsImg\/)/i, "comicsImg/");

                const coverDiv = document.createElement("div");
                coverDiv.className = "cover";
                coverDiv.innerHTML = `
                    <img src="${rutaRelativa}" alt="Cover">
                    <p>${cover.ilustracion}</p>
                    <span>$${cover.precio}</span>
                `;
                coversContainer.appendChild(coverDiv);
            });

            coversModal.style.display = "flex";
        } catch (err) {
            coversContainer.innerHTML = `<p>Error al cargar portadas: ${err}</p>`;
        }
    }

    // Cerrar modal
    closeModalBtn.addEventListener("click", () => coversModal.style.display = "none");
    window.addEventListener("click", e => {
        if (e.target === coversModal) coversModal.style.display = "none";
    });

    // ===== Cargar cómics =====
    async function loadComics() {
        try {
            const res = await fetch("backend/get_comics.php");
            const comics = await res.json();

            for (const comic of comics) {
                const coversRes = await fetch(`backend/get_covers.php?comic_id=${comic.id}&api_key=${API_KEY}`);
                const covers = await coversRes.json();
                comic.covers = Array.isArray(covers) ? covers : [];

                const comicHTML = createComicHTML(comic);
                newComicsRow.appendChild(comicHTML);
            }
        } catch (err) {
            console.error("Error al cargar comics:", err);
        }
    }

    loadComics();

    // ===== Carrusel de banners =====
    const items = document.querySelectorAll(".carousel-item");
    let current = 0;

    function showSlide(index) {
        items.forEach((item, i) => item.classList.toggle("active", i === index));
    }

    document.querySelector(".carousel-btn.prev").addEventListener("click", () => {
        current = (current - 1 + items.length) % items.length;
        showSlide(current);
    });

    document.querySelector(".carousel-btn.next").addEventListener("click", () => {
        current = (current + 1) % items.length;
        showSlide(current);
    });

    setInterval(() => {
        current = (current + 1) % items.length;
        showSlide(current);
    }, 5000);

    // ===== Menú lateral =====
    const sideMenu = document.getElementById("side-menu");
    document.querySelector(".hamburger").addEventListener("click", () => sideMenu.style.left = "0");
    document.getElementById("close-menu").addEventListener("click", () => sideMenu.style.left = "-250px");

    // ===== Dropdown "Mi cuenta" =====
    const userMenuBtn = document.querySelector(".user-menu button");
    const dropdown = document.querySelector(".user-menu .dropdown");

    userMenuBtn.addEventListener("click", () => {
        dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    });

    window.addEventListener("click", e => {
        if (!e.target.closest(".user-menu")) dropdown.style.display = "none";
    });
});
