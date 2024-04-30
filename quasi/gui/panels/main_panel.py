import flet as ft

from quasi.gui.board.board import Board
from quasi.gui.bar.simulation_bar import SimulationBar
from quasi.gui.board.info_bar import InfoBar
from quasi.gui.panels.documentation_panel import DocumentationTab
from quasi.gui.report import Report


class MainPanel(ft.UserControl):

    __instance = None

    def __init__(self, page: ft.Page):
        super().__init__()
        MainPanel.__instance = self
        self.simulation_bar = SimulationBar()
        self.info_bar = InfoBar()
        self.info_bar.set_page(page)
        self.tabs = ft.Tabs(
            on_change=self.on_change,
            tab_alignment=ft.TabAlignment.START,
            indicator_color="white",
            divider_color="black",
            unselected_label_color="white",
            indicator_padding=0,
            indicator_tab_size=5,
            label_color="blue",
            tabs=[
                ft.Tab(
                    text="Board",
                    content=ft.Stack(
                        [
                            ft.Container(
                                top=0,
                                left=0,
                                right=0,
                                bottom=0,
                                content=ft.Stack(
                                    [
                                        Board(self.page),
                                        self.simulation_bar,
                                        self.info_bar
                                    ]
                                ))]
                    )
                ),
                ft.Tab(
                    text="Report",
                    content=Report()
                ),
            ]
        )

        self.tabs_container=ft.Container(
            top=25,
            bottom=0,
            left=0,
            right=0,
            content=self.tabs
        )
        self.container=ft.Stack(
            [ft.Container(
                top=0,
                left=0,
                right=0,
                bottom=0,
                bgcolor="#130925",
            ),
             self.tabs_container
             ]
        )

    @classmethod
    def get_instance(cls):
        return MainPanel.__instance
        
    def build(self) -> ft.Container:
        return self.container

    def on_change(self, e):
        print("change")
        print(f"name: {e.name}")
        print(f"target: {e.target}")
        print(f"data: {e.data}")
        print(self)
        r = Report()
        print(f"{e.data}==1, {e.data == 1}, {type(e.data)}")
        if int(e.data) == 1:
            r.on_visible_changed(visible=True)
        else:
            r.on_visible_changed(visible=False)
            


    def new_documentation_tab(self, documentation_tab):
        self.tabs.tabs.append(documentation_tab.build())
        self.container.update()
        

    