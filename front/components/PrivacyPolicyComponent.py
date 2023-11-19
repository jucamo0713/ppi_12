# Importaciones de librerías de terceros
import streamlit as st


def privacy_policy_component():
    """
    Muestra el componente de política de privacidad de LitWave en un formato
    legible en Streamlit.

    Este componente utiliza las funciones de Streamlit para presentar de
    manera organizada la política de privacidad de uso de LitWave.

    Returns:
        None
    """
    st.title("Política de Privacidad")
    st.write("Última actualización: 27 de octubre de 2023")
    st.write(
        "Esta Política de Privacidad describe nuestras políticas y "
        "procedimientos sobre la recopilación, el uso y la divulgación "
        "de su información cuando utiliza el Servicio y le informa sobre sus "
        "derechos de privacidad y cómo la ley lo protege.")

    st.write(
        "Utilizamos sus datos personales para proporcionar y mejorar el "
        "Servicio. Al utilizar el Servicio, usted acepta la recopilación y el "
        "uso de información de acuerdo con esta Política de Privacidad.")

    st.header("Interpretación y Definiciones")

    st.subheader("Interpretación")
    st.write(
        "Las palabras cuya letra inicial está en mayúscula tienen "
        "significados definidos en las siguientes condiciones. Las siguientes "
        "definiciones tendrán el mismo significado, ya aparezcan en singular "
        "o en plural.")

    st.subheader("Definiciones")
    st.write("A los efectos de esta Política de Privacidad:")

    definitions = {
        "Cuenta": "significa una cuenta única creada para que usted acceda "
                  "a nuestro Servicio o partes de nuestro Servicio.",
        "Afiliado": "significa una entidad que controla, es controlada por "
                    "o está bajo control común con una parte, donde 'control' "
                    "significa la propiedad del 50% o más de las acciones,"
                    " participación en el capital u otros valores con derecho "
                    "a voto para la elección de directores u otra autoridad "
                    "de gestión.",
        "Compañía": "se refiere a LitWave.",
        "Cookies": "son archivos pequeños que se colocan en su computadora, "
                   "dispositivo móvil o cualquier otro dispositivo por un "
                   "sitio web, que contiene los detalles de su historial "
                   "de navegación en ese sitio web entre sus muchos usos.",
        "País": "se refiere a: Colombia.",
        "Dispositivo": "significa cualquier dispositivo que pueda acceder al "
                       "Servicio, como una computadora, un teléfono celular o "
                       "una tableta digital.",
        "Datos Personales": "cualquier información que se relacione con una "
                            "persona identificada o identificable.",
        "Servicio": "se refiere al Sitio web.",
        "Proveedor de Servicios": "significa cualquier persona natural o "
                                  "jurídica que procesa los datos en nombre "
                                  "de la Compañía. Se refiere a empresas o "
                                  "individuos de terceros empleados por la "
                                  "Compañía para facilitar el Servicio, "
                                  "proporcionar el Servicio en nombre de la "
                                  "Compañía, realizar servicios relacionados "
                                  "con el Servicio o ayudar a la Compañía en "
                                  "el análisis de cómo se utiliza el servicio",
        "Datos de Uso": "se refiere a datos recopilados automáticamente, ya "
                        "sea generados por el uso del Servicio o desde la "
                        "infraestructura del Servicio en sí (por ejemplo, la "
                        "duración de una visita a la página).",
        "Sitio web": "se refiere a LitWave, accesible desde "
                     "[https://litwave.streamlit.app/]"
                     "(https://litwave.streamlit.app/).",
        "Usted": "significa la persona que accede o utiliza el Servicio, o "
                 "la empresa u otra entidad legal en nombre de la cual esa "
                 "persona accede o utiliza el Servicio, según corresponda."
    }

    for term, definition in definitions.items():
        st.write(f"- **{term}**: {definition}")

    st.header("Recopilación y Uso de sus Datos Personales")

    st.subheader("Tipos de Datos Recopilados")

    st.subheader("Datos Personales")
    st.write(
        "Mientras utiliza nuestro Servicio, es posible que le pidamos que nos "
        "proporcione cierta información de identificación personal que se "
        "puede utilizar para contactarlo o identificarlo. La información de "
        "identificación personal puede incluir, entre otras cosas:")

    personal_data_list = ["Dirección de correo electrónico",
                          "Nombre y apellido", "Datos de uso"]

    for item in personal_data_list:
        st.write(f"- {item}")

    st.subheader("Datos de Uso")
    st.write(
        "Los Datos de Uso se recopilan automáticamente al utilizar el "
        "Servicio.")
    st.write(
        "Los Datos de Uso pueden incluir información como la dirección IP de "
        "su dispositivo (por ejemplo, dirección IP), tipo de navegador, "
        "versión del navegador, las páginas de nuestro Servicio que visita, "
        "la fecha y hora de su visita, el tiempo que pasa en esas páginas, "
        "identificadores de dispositivos únicos y otros datos diagnósticos.")

    st.write(
        "Cuando accede al Servicio a través de un dispositivo móvil, podemos "
        "recopilar automáticamente cierta información, incluido, entre "
        "otros, el tipo de dispositivo móvil que utiliza, la ID única de su "
        "dispositivo móvil, la dirección IP de su dispositivo móvil, el "
        "sistema operativo móvil de su dispositivo, el tipo de navegador de "
        "Internet móvil que utiliza, identificadores de dispositivos únicos y "
        "otros datos diagnósticos.")

    st.write(
        "También podemos recopilar información que su navegador envía cada "
        "vez que visita nuestro Servicio o cuando accede al Servicio a través "
        "de un dispositivo móvil.")

    st.subheader("Tecnologías de Rastreo y Cookies")

    st.write(
        "Utilizamos Cookies y tecnologías de seguimiento similares para "
        "rastrear la actividad en nuestro Servicio y almacenar cierta "
        "información. Las tecnologías de seguimiento utilizadas pueden "
        "incluir balizas, etiquetas y scripts para recopilar y rastrear "
        "información y para mejorar y analizar nuestro Servicio. Las "
        "tecnologías que utilizamos pueden incluir:")

    tracking_technologies_list = (["Cookies o Cookies del Navegador.",
                                  "Web Beacons."])

    for item in tracking_technologies_list:
        st.write(f"- {item}")

    st.write("Las Cookies pueden ser 'Persistentes' o 'de Sesión'. Las "
             "Cookies Persistentes permanecen en su computadora personal o "
             "dispositivo móvil cuando se desconecta, mientras que las "
             "Cookies de Sesión se eliminan tan pronto como cierra su "
             "navegador web.")

    st.write("Utilizamos tanto Cookies de Sesión como Persistentes con los "
             "siguientes propósitos:")

    purposes_list = [
        "Cookies Necesarias / Esenciales: Estas Cookies son esenciales para "
        "proporcionarle servicios disponibles a través del Sitio web y para "
        "permitirle utilizar algunas de sus funciones. Ayudan a autenticar a "
        "los usuarios y a prevenir el uso fraudulento de las cuentas de "
        "usuario.",
        "Cookies de Aceptación de Política / Aviso: Estas Cookies "
        "identifican si los usuarios han aceptado el uso de cookies en el "
        "Sitio web.",
        "Cookies de Funcionalidad: Estas Cookies nos permiten recordar las "
        "opciones que hace cuando utiliza el Sitio web, como recordar sus "
        "detalles de inicio de sesión o preferencia de idioma. El propósito "
        "de estas Cookies es proporcionarle una experiencia más personalizada "
        "y evitar que tenga que volver a ingresar sus preferencias cada vez "
        "que use el Sitio web."
    ]

    for item in purposes_list:
        st.write(f"- {item}")

    st.subheader("Uso de sus Datos Personales")

    st.write("La Compañía puede utilizar Datos Personales para los siguientes "
             "fines:")

    data_usage_list = [
        "Para proporcionar y mantener nuestro Servicio, incluido el monitoreo "
        "del uso de nuestro Servicio.",
        "Para gestionar su Cuenta: para gestionar su registro como usuario "
        "del Servicio. Los Datos Personales que proporciona pueden darle "
        "acceso a diferentes funcionalidades del Servicio que están "
        "disponibles para usted como usuario registrado.",
        "Para el cumplimiento de un contrato: el desarrollo, cumplimiento y "
        "realización del contrato de compra de los productos, artículos o "
        "servicios que ha comprado o de cualquier otro contrato con nosotros "
        "a través del Servicio.",
        "Para contactarlo: para contactarlo por correo electrónico, llamadas "
        "telefónicas, mensajes de texto (SMS) u otras formas equivalentes de "
        "comunicación electrónica, como notificaciones push de aplicaciones "
        "móviles sobre actualizaciones o comunicaciones informativas "
        "relacionadas con las funcionalidades, productos o servicios "
        "contratados, incluidas las actualizaciones de seguridad, cuando sea "
        "necesario o razonable para su implementación.",
        "Para proporcionarle noticias, ofertas especiales e información "
        "general sobre otros bienes, servicios y eventos que ofrecemos y que "
        "son similares a los que ya ha comprado o preguntado, a menos que "
        "haya optado por no recibir dicha información.",
        "Para gestionar sus solicitudes: para atender y gestionar sus "
        "solicitudes hacia nosotros.",
        "Para transferencias comerciales: podemos utilizar su información "
        "para evaluar o llevar a cabo una fusión, venta de activos de la "
        "empresa, financiamiento o adquisición de todo o parte de nuestro "
        "negocio por otra empresa.",
        "Para otros fines: podemos utilizar su información para otros fines, "
        "como análisis de datos, identificación de tendencias de uso, "
        "determinación de la efectividad de nuestras campañas promocionales "
        "y para evaluar y mejorar nuestro Servicio, productos, servicios, "
        "marketing y su experiencia."
    ]

    for item in data_usage_list:
        st.write(f"- {item}")

    st.write("Podemos compartir su información personal en las siguientes "
             "situaciones:")

    data_sharing_list = [
        "Con Proveedores de Servicios: podemos compartir su información "
        "personal con Proveedores de Servicios para monitorear y analizar el "
        "uso de nuestro Servicio, para contactarlo.",
        "Para transferencias comerciales: podemos compartir o transferir su "
        "información personal en relación con, o durante negociaciones de, "
        "cualquier fusión, venta de activos de la Compañía, financiamiento o "
        "adquisición de todo o parte de nuestro negocio por otra empresa.",
        "Con Afiliados: podemos compartir su información con nuestros "
        "afiliados, en cuyo caso requeriremos que esos afiliados cumplan con "
        "esta Política de Privacidad. Los afiliados incluyen nuestra empresa "
        "matriz y cualquier otra subsidiaria, socios de empresas conjuntas u "
        "otras empresas que controlemos o que estén bajo control común con "
        "nosotros.",
        "Con socios comerciales: podemos compartir su información con "
        "nuestros socios comerciales para ofrecerle ciertos productos, "
        "servicios o promociones.",
        "Con otros usuarios: cuando comparte información personal o "
        "interactúa de otra manera en las áreas públicas con otros usuarios, "
        "dicha información puede ser vista por todos los usuarios y puede ser "
        "distribuida públicamente fuera de ellas.",
        "Con su consentimiento: podemos divulgar su información personal para "
        "cualquier otro propósito con su consentimiento."
    ]

    for item in data_sharing_list:
        st.write(f"- {item}")

    st.subheader("Retención de sus Datos Personales")

    st.write(
        "La Compañía retendrá sus Datos Personales solo durante el tiempo que "
        "sea necesario para los fines establecidos en esta Política de "
        "Privacidad. Retendremos y utilizaremos sus Datos Personales en la "
        "medida necesaria para cumplir con nuestras obligaciones legales "
        "(por ejemplo, si estamos obligados a retener sus datos para cumplir "
        "con las leyes aplicables), resolver disputas y hacer cumplir nuestros"
        " acuerdos legales y políticas.")

    st.write(
        "La Compañía también retendrá Datos de Uso con fines de análisis "
        "interno. Los Datos de Uso generalmente se retienen por un período de "
        "tiempo más corto, excepto cuando estos datos se utilizan para "
        "fortalecer la seguridad o mejorar la funcionalidad de nuestro "
        "Servicio, o cuando estamos legalmente obligados a retener estos "
        "datos por períodos de tiempo más largos.")

    st.subheader("Transferencia de sus Datos Personales")

    st.write(
        "Su información, incluidos los Datos Personales, se procesa en las "
        "oficinas operativas de la Compañía y en cualquier otro lugar donde "
        "se encuentren las partes involucradas en el procesamiento. Esto "
        "significa que esta información puede ser transferida y mantenida en "
        "computadoras ubicadas fuera de su estado, provincia, país u otra "
        "jurisdicción gubernamental donde las leyes de protección de datos "
        "pueden diferir de las de su jurisdicción.")

    st.write(
        "Su consentimiento a esta Política de Privacidad seguido de su envío "
        "de dicha información representa su acuerdo con esa transferencia.")

    st.write(
        "La Compañía tomará todas las medidas razonablemente necesarias para "
        "garantizar que sus datos se traten de manera segura y de acuerdo con "
        "esta Política de Privacidad, y ninguna transferencia de sus Datos "
        "Personales tendrá lugar a una organización o país a menos que "
        "existan controles adecuados, incluida la seguridad de sus datos y "
        "otra información personal.")

    st.subheader("Eliminar sus Datos Personales")

    st.write(
        "Usted tiene el derecho de eliminar o solicitar que ayudemos a "
        "eliminar los Datos Personales que hemos recopilado sobre usted.")

    st.write(
        "Nuestro Servicio puede brindarle la capacidad de eliminar cierta "
        "información sobre usted desde dentro del Servicio.")

    st.write(
        "Puede actualizar, modificar o eliminar su información en cualquier "
        "momento iniciando sesión en su Cuenta, si la tiene, y visitando la "
        "sección de configuración de la cuenta que le permite administrar su "
        "información personal. También puede ponerse en contacto con nosotros "
        "para solicitar acceso, corrección o eliminación de cualquier "
        "información personal que nos haya proporcionado.")

    st.write(
        "Tenga en cuenta, sin embargo, que es posible que debamos retener "
        "cierta información cuando tengamos una obligación legal o base legal "
        "para hacerlo.")

    st.subheader("Divulgación de sus Datos Personales")

    st.write("La Compañía puede compartir su información personal en las "
             "siguientes situaciones:")

    st.write("- Con Proveedores de Servicios: Podemos compartir su "
             "información personal con Proveedores de Servicios para "
             "monitorear y analizar el uso de nuestro Servicio, y para "
             "contactarlo.")
    st.write("- En caso de transacciones comerciales: Podemos compartir o "
             "transferir su información personal en relación con, o durante "
             "negociaciones de, cualquier fusión, venta de activos de la "
             "Compañía, financiamiento o adquisición de todo o parte de "
             "nuestro negocio por otra empresa.")
    st.write("- Con Afiliados: Podemos compartir su información con nuestros "
             "afiliados, en cuyo caso les exigiremos a esos afiliados que "
             "cumplan con esta Política de Privacidad. Los afiliados incluyen "
             "nuestra empresa matriz y cualquier otra subsidiaria, socio de "
             "empresa conjunta u otras empresas que controlemos o que estén "
             "bajo control común con nosotros.")
    st.write("- Con socios comerciales: Podemos compartir su información con "
             "nuestros socios comerciales para ofrecerle ciertos productos, "
             "servicios o promociones.")
    st.write("- Con otros usuarios: cuando comparte información personal o "
             "interactúa en áreas públicas con otros usuarios, dicha "
             "información puede ser vista por todos los usuarios y puede ser "
             "distribuida públicamente fuera.")
    st.write("- Con su consentimiento: Podemos divulgar su información "
             "personal para cualquier otro propósito con su consentimiento.")

    st.subheader("Seguridad de sus Datos Personales")

    st.write("La seguridad de sus Datos Personales es importante para "
             "nosotros, pero recuerde que ningún método de transmisión "
             "por Internet o método de almacenamiento electrónico es 100% "
             "seguro. Si bien nos esforzamos por utilizar medios "
             "comercialmente aceptables para proteger sus Datos Personales, "
             "no podemos garantizar su seguridad absoluta.")

    st.subheader("Privacidad de los Niños")

    st.write("Nuestro Servicio no está dirigido a personas menores de 13 "
             "años. No recopilamos conscientemente información personal "
             "identificable de nadie menor de 13 años. Si usted es "
             "padre/madre o tutor y sabe que su hijo nos ha proporcionado "
             "Datos Personales, comuníquese con nosotros. Si nos damos cuenta "
             "de que hemos recopilado Datos Personales de menores de 13 años "
             "sin verificación del consentimiento parental, tomamos medidas "
             "para eliminar esa información de nuestros servidores.")

    st.write("Si necesitamos depender del consentimiento como base legal para "
             "procesar su información y su país requiere el consentimiento de "
             "un padre, podemos solicitar el consentimiento de sus padres "
             "antes de recopilar y usar esa información.")

    st.subheader("Enlaces a Otros Sitios Web")

    st.write("Nuestro Servicio puede contener enlaces a otros sitios web que "
             "no son operados por nosotros. Si hace clic en un enlace de un "
             "tercero, será dirigido al sitio de ese tercero. Le recomendamos "
             "encarecidamente que revise la Política de Privacidad de cada "
             "sitio que visite.")

    st.write("No tenemos control ni asumimos responsabilidad por el "
             "contenido, las políticas de privacidad o las prácticas de "
             "sitios o servicios de terceros.")

    st.subheader("Cambios a esta Política de Privacidad")

    st.write("Podemos actualizar nuestra Política de Privacidad de vez en "
             "cuando. Le notificaremos cualquier cambio publicando la nueva "
             "Política de Privacidad en esta página.")

    st.write("Le informaremos por correo electrónico y/o mediante un aviso "
             "destacado en nuestro Servicio antes de que el cambio entre en "
             "vigencia y actualizaremos la fecha de 'Última actualización' "
             "en la parte superior de esta Política de Privacidad.")

    st.write("Le recomendamos que revise esta Política de Privacidad "
             "periódicamente para cualquier cambio. Los cambios a esta "
             "Política de Privacidad son efectivos cuando se publican en esta "
             "página.")

    st.subheader("Contáctenos")

    st.write("Si tiene alguna pregunta sobre esta Política de Privacidad, "
             "puede ponerse en contacto con nosotros:")

    st.write("- Visitando esta página en nuestro sitio web: "
             "[Sobre nosotros]"
             "(https://litwave.streamlit.app/Sobre_nosotros)")
