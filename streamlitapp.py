import hydralit as hy
from hydralit import HydraApp
import apps.home_app
from functions.database import create_tables, create_db
from forms.logon import login_form
import apps

if 'logged_in' not in hy.session_state:
        hy.session_state['logged_in'] = False
    
if 'role' not in hy.session_state:
        hy.session_state['role'] = '5'

@hy.dialog("Login")
def show_login_form() -> None:
    create_db()
    create_tables()
    login_form()

if __name__ == '__main__':

    over_theme = {'menu_background': '#5190f2'}

    app = HydraApp(
            title = "KRFC Player Development Tracker",
            favicon="",
            hide_streamlit_markers=True,
            use_banner_images=["./assets/banner.png",None,{'header': "<h1 style = 'text-align=centre; padding: 0px 0px; color:DodgerBlue; font-size:20%;'>The Power to Perform!</h1><br>"},None,"./assets/icon.png"],
            banner_spacing=[50,5,50,48,7],
            use_navbar=True,
            navbar_sticky=True,
            navbar_animation=True,
            navbar_theme=over_theme,
    )

    app.add_app("Home", icon="bi bi-house-fill", app=apps.HomeApp(title="Home"),is_home=True)

    app.add_app("Admin", icon="bi bi-gear-fill", app=apps.AdminApp(title="Admin"))
    app.add_app("Teams", icon="bi bi-person-badge", app=apps.TeamsApp(title="Teams"))
    app.add_app("Dashboard", icon="bi bi-person-badge", app=apps.DashboardApp(title="Dashboard"))

    @app.login_callback
    def mylogin_cb():
        show_login_form()
    
    role = hy.session_state["role"]
    if len(role) > 1 and role[1] == "1":
        complex_nav = {
            "Home": ["Home"],
            "Admin": ["Admin"],
            "Teams": ["Teams"],
            "Dashboard": ["Dashboard"]
        }
    elif role[0] == "5":
        complex_nav = {
            "Home": ["Home"]
        }
    else:
        complex_nav = {
            "Home": ["Home"],
            "Teams": ["Teams"],
            "Dashboard": ["Dashboard"]
        }

    app.run(complex_nav)
    