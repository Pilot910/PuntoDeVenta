<?php include("backend/db_connect.php"); ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Comic Store México</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="js/main.js" defer></script>
    <link rel="icon" href="img/logo.png" type="image/png">
</head>
<body>
    <header>
        <div class="header-left">
            <button class="hamburger">☰</button>
            <a href="#" class="logo"><img src="img/logo.png" alt="Logo"></a>
        </div>
        <div class="header-center">
            <div class="search-bar">
                <input type="text" placeholder="Buscar cómic...">
            </div>
        </div>
        <div class="header-right">
            <button class="cart">🛒 Carrito</button>
            <div class="user-menu">
                <button>Mi cuenta ▼</button>
                <div class="dropdown">
                    <a href="#">Iniciar sesión</a>
                    <a href="#">Crear cuenta</a>
                </div>
            </div>
        </div>
    </header>

    <main>
        <!-- Carrusel -->
        <div class="carousel">
            <div class="carousel-item active">
                <img src="img/banner1.jpg" alt="Banner 1">
            </div>
            <div class="carousel-item">
                <img src="img/banner2.jpeg" alt="Banner 2">
            </div>
            <div class="carousel-item">
                <img src="img/banner3.jpeg" alt="Banner 3">
            </div>
            <button class="carousel-btn prev">&#10094;</button>
            <button class="carousel-btn next">&#10095;</button>
        </div>

        <!-- Catálogo -->
        <section class="catalog">
            <h2>Más nuevo en tienda</h2>
            <div class="row-wrapper">
                <button id="new-prev" class="row-btn prev" aria-label="Anterior">‹</button>
                <div class="comic-row" id="new-comics"></div>
                <button id="new-next" class="row-btn next" aria-label="Siguiente">›</button>
            </div>

            <h2>Destacados</h2>
            <div class="comic-row" id="featured-comics"></div>

            <h2>Próximamente</h2>
            <div class="comic-row" id="upcoming-comics"></div>

            <h2>Recomendaciones</h2>
            <div class="comic-row" id="recommended-comics"></div>
        </section>
    </main>

    <footer>
        <div class="footer-links">
            <a href="#">Inicio</a> | 
            <a href="#">Catálogo</a> | 
            <a href="#">Editoriales</a> | 
            <a href="#">Políticas</a>
        </div>
        <div class="footer-contact">
            contacto@comicsmexico.com | +52 55 3453 7823
        </div>
        <div>
            Av. Revolución 50, Mexico City, Mexico
        </div>
    </footer>

    <!-- Menú lateral -->
    <nav id="side-menu" class="side-menu">
        <button id="close-menu" class="close-btn">×</button>
        <ul>
            <li><a href="#">Marvel</a></li>
            <li><a href="#">DC</a></li>
            <li><a href="#">Image Comics</a></li>
            <li><a href="#">Contacto</a></li>
        </ul>
    </nav>

    <!-- Modal para portadas -->
    <div id="covers-modal" class="modal" style="display:none;">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h3 id="modal-title">Portadas</h3>
            <div class="covers-row" id="covers-container"></div>
        </div>
    </div>
</body>
</html>
