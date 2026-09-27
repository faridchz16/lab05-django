import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie, Rating

HOLLYWOOD_DATA = {
    "Inception": {
        "description": "Dom Cobb es un ladrón experimentado, el mejor en el peligroso arte de la extracción: robar secretos del subconsciente durante el sueño. Para recuperar su vida y regresar con sus hijos, debe liderar un equipo en una misión inversa casi imposible: implantar una idea en la mente de un heredero empresarial.",
        "ratings": [
            ("IMDb_Critic", 9, "Una obra maestra que redefine el cine de ciencia ficción moderno."),
            ("Rotten_Tomatoes", 9, "Efectos visuales revolucionarios y un guion cerebral brillante."),
            ("Metacritic", 9, "Dirección monumental de Christopher Nolan y banda sonora legendaria de Hans Zimmer."),
            ("Rolling_Stone", 8, "Una experiencia cinematográfica electrizante y compleja."),
            ("The_Guardian", 9, "Narrativa multinivel ejecutada con maestría técnica absoluta.")
        ]
    },
    "Interstellar": {
        "description": "En un futuro donde la Tierra enfrenta una devastadora crisis climática y hambruna, un grupo de valientes astronautas y científicos viaja a través de un agujero de gusano cerca de Saturno en busca de un planeta habitable que garantice la supervivencia de la especie humana.",
        "ratings": [
            ("IMDb_Critic", 9, "Una odisea espacial visualmente deslumbrante con un corazón profundamente humano."),
            ("Variety", 9, "La física relativista y el amor trascienden dimensiones en este clásico moderno."),
            ("Empire", 8, "Ambiciosa, emocionalmente abrumadora y con una escala visual sin precedentes.")
        ]
    },
    "The Dark Knight": {
        "description": "Batman, junto al fiscal de distrito Harvey Dent y el teniente Jim Gordon, busca erradicar el crimen organizado en Gotham City. Sin embargo, la inesperada aparición del Joker, un genio anarquista del caos, empuja al Caballero Oscuro al límite moral y psicológico.",
        "ratings": [
            ("IMDb_Critic", 9, "La cumbre indiscutible del cine de superhéroes y del thriller psicológico."),
            ("Chicago_Sun_Times", 9, "La inolvidable actuación de Heath Ledger como el Joker es histórica."),
            ("Sight_&_Sound", 9, "Un relato magistral sobre el orden, el caos y la corrupción del alma humana.")
        ]
    },
    "Pulp Fiction": {
        "description": "Una obra maestra no lineal que conecta las vidas de dos sicarios filosóficos, la seductora esposa de un jefe criminal, un boxeador en problemas y dos asaltantes novatos en el inframundo criminal de Los Ángeles, cargada de humor negro y diálogos icónicos.",
        "ratings": [
            ("IMDb_Critic", 9, "Palma de Oro en Cannes y pieza fundacional del cine independiente contemporáneo."),
            ("Roger_Ebert", 9, "Diálogos electrizantes, estructura audaz y un estilo inconfundible."),
            ("Cahiers_du_Cinema", 9, "Tarantino reinventa el género negro con audacia revolucionaria."),
            ("Film_Comment", 9, "Iconografía pop atemporal y actuaciones memorables."),
            ("Time_Magazine", 8, "Entretenimiento puro con filo artístico implacable.")
        ]
    },
    "Django Unchained": {
        "description": "Dos años antes de la Guerra Civil estadounidense, el doctor King Schultz, un cazarrecompensas alemán, libera al esclavo Django. Juntos emprenden una peligrosa travesía por el sur para cazar criminales y rescatar a Broomhilda, la esposa cautiva de Django, del sádico terrateniente Calvin Candie.",
        "ratings": [
            ("IMDb_Critic", 9, "Un western visceral lleno de adrenalina, justicia poética y genialidad actoral."),
            ("Hollywood_Reporter", 8, "Christoph Waltz y Leonardo DiCaprio brillan en este épico homenaje al spaguetti western.")
        ]
    },
    "Jurassic Park": {
        "description": "Un magnate crea un parque temático revolucionario en una isla remota habitado por dinosaurios reales clonados mediante ADN prehistórico. Sin embargo, un acto de espionaje industrial desactiva los sistemas de contención eléctrica, desatando el pánico y la lucha por sobrevivir.",
        "ratings": [
            ("IMDb_Critic", 8, "Marcó un antes y un después en los efectos especiales de Hollywood."),
            ("New_York_Times", 8, "Spielberg construye un espectáculo sobrecogedor y aterrador por igual."),
            ("Entertainment_Weekly", 8, "Pura magia cinematográfica y tensión dosificada con maestría."),
            ("Total_Film", 9, "Una aventura atemporal que asombra a cada nueva generación."),
            ("Empire", 8, "Un hito definitivo de la cultura pop y la ciencia ficción comercial.")
        ]
    },
    "Schindler's List": {
        "description": "Basada en hechos reales, narra la historia de Oskar Schindler, un carismático empresario alemán afiliado al partido nazi que, conmovido por las atrocidades del Holocausto en Cracovia, arriesga toda su fortuna personal para salvar a más de 1.100 judíos de las cámaras de gas.",
        "ratings": [
            ("Academy_Awards", 9, "Ganadora de 7 premios Óscar, incluyendo Mejor Película y Mejor Director."),
            ("Washington_Post", 9, "Un testimonio cinematográfico desgarrador, necesario e inolvidable."),
            ("BBC_Culture", 9, "La obra magna de Steven Spielberg filmada en un conmovedor blanco y negro.")
        ]
    },
    "Superbad": {
        "description": "Seth y Evan son dos inseparables estudiantes de último año de instituto marginados socialmente. Cuando son invitados a una fiesta universitaria, prometen conseguir alcohol ilegal con un documento de identidad falso a nombre de 'McLovin', desencadenando una de las noches más caóticas y disparatadas de sus vidas.",
        "ratings": [
            ("IMDb_Critic", 8, "Una comedia generacional inolvidable con un corazón entrañable."),
            ("Rolling_Stone", 7, "Divertidísima de principio a fin, el humor adolescente llevado a su mejor versión."),
            ("IndieWire", 8, "El personaje de McLovin es una leyenda absoluta de la comedia juvenil."),
            ("Los_Angeles_Times", 7, "Captura con autenticidad y vulgaridad honesta el final de la adolescencia."),
            ("Total_Film", 8, "Guion ingenioso de Seth Rogen y química insuperable entre Cera y Hill.")
        ]
    },
    "Blade Runner 2049": {
        "description": "Treinta años después de los acontecimientos de la obra original, el oficial K, un replicante de la policía de Los Ángeles, desentierra un enigma largamente oculto que tiene el poder de sumergir lo que queda de la civilización en una guerra. Su descubrimiento lo obliga a rastrear a Rick Deckard, desaparecido hace décadas.",
        "ratings": [
            ("IMDb_Critic", 8, "Una obra de arte visualmente hipnótica con la fotografía premiada de Roger Deakins."),
            ("Screen_Daily", 8, "Denis Villeneuve logra el milagro de honrar y expandir el mito de Blade Runner."),
            ("The_Telegraph", 8, "Filosofía existencialista y atmósfera cyberpunk de altísima factura.")
        ]
    },
    "Arrival": {
        "description": "Cuando doce misteriosas naves extraterrestres descienden sobre la Tierra, la lingüista experta Louise Banks es reclutada por el ejército de EE.UU. para interpretar el complejo idioma no lineal de los visitantes y descubrir si representan una amenaza o una ofrenda para la humanidad antes de que estalle un conflicto armado global.",
        "ratings": [
            ("IMDb_Critic", 8, "Ciencia ficción profunda e intelectual sobre el tiempo, el dolor y la comunicación."),
            ("Boston_Globe", 8, "Amy Adams entrega una de las actuaciones más sutiles y conmovedoras de su carrera."),
            ("The_Atlantic", 8, "Un enfoque reflexivo y humanista que rompe los clichés de invasiones alienígenas."),
            ("Village_Voice", 8, "Emocionante, trascendental y con un giro argumental deslumbrante."),
            ("Slate", 7, "Demuestra cómo el lenguaje puede moldear la percepción de nuestra existencia.")
        ]
    }
}

def update_data():
    for title, data in HOLLYWOOD_DATA.items():
        movie = Movie.objects.filter(title=title).first()
        if movie:
            movie.description = data["description"]
            movie.save()
            
            # Replace ratings with accurate Hollywood critic scores
            movie.ratings.all().delete()
            for user, score, comment in data["ratings"]:
                Rating.objects.create(
                    movie=movie,
                    user_name=user,
                    score=score,
                    comment=comment
                )
            print(f"Updated Hollywood data for: {title}")

if __name__ == '__main__':
    update_data()
