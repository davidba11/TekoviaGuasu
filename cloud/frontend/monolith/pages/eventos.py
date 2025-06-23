# pages/eventos.py
import reflex as rx
from datetime import date
from controllers.event_state import EventState

BG = "#FFF8E7"
BLUE = "#0033A0"
RED = "#D22630"
GRAY_DARK = "#4A4A4A"
HEADERS = ["Título", "Fecha", "Ciudad", "Categoría", "Acciones"]

@rx.page(route="/", on_load=[EventState.load])
def eventos() -> rx.Component:

    def row(ev):
        return rx.table.row(
            rx.table.cell(ev["titulo"], color="#0D0D0D"),
            rx.table.cell(ev["fecha"], color="#0D0D0D"),
            rx.table.cell(ev["ciudad"], color="#0D0D0D"),
            rx.table.cell(ev["categoria"], color="#0D0D0D"),
            rx.table.cell(
                rx.hstack(
                    rx.icon_button(
                        "pencil",
                        on_click=lambda: EventState.edit_event(ev["id"]),
                        color_scheme="red",
                        variant="ghost"
                    ),
                    rx.icon_button(
                        "trash",
                        on_click=lambda: EventState.show_delete_modal(ev["id"], ev["titulo"]),
                        color_scheme="red",
                        variant="ghost"
                    ),
                ),
                width="1%",
            ),
            bg="#F4F6FC",
            _hover=dict(bg="#D9E6FF"),
            border_bottom="1px solid #E0E0E0"
        )

    nav = rx.hstack(
        rx.button(
            "Anterior",
            on_click=EventState.prev_page,
            is_disabled=EventState.offset <= 0,
            bg=RED, color="white",
        ),
        rx.text(
            EventState.current_page, " / ", EventState.num_total_pages,
            font_weight="bold",
            color=RED,
        ),
        rx.button(
            "Siguiente",
            on_click=EventState.next_page,
            is_disabled=EventState.offset + EventState.limit >= EventState.total_items,
            bg=RED, color="white",
        ),
        justify="center",
        spacing="4",
        width="100%",
    )

    return rx.box(
        rx.vstack(
            rx.text("Calendario Cultural — Tekovia Guasu", size="8", weight="bold", color=BLUE),

            rx.form(
                rx.vstack(
                    rx.text(
                        "Registro y visualización de eventos municipales",
                        font_weight="bold",
                        color=BLUE,
                        align="center",
                    ),
                    rx.hstack(
                        rx.input(
                            id="titulo",
                            placeholder="Título",
                            value=EventState.form_data["titulo"],
                            on_change=lambda e: EventState.set_form_field("titulo", e),
                            w="25%", placeholder_text_color=GRAY_DARK
                        ),
                        rx.input(
                            id="fecha",
                            type_="date",
                            value=rx.cond(
                                EventState.form_data["fecha"] != "",
                                EventState.form_data["fecha"],
                                date.today().isoformat()
                            ),
                            on_change=lambda e: EventState.set_form_field("fecha", e),
                            w="25%"
                        ),
                        rx.input(
                            id="ciudad",
                            placeholder="Ciudad",
                            value=EventState.form_data["ciudad"],
                            on_change=lambda e: EventState.set_form_field("ciudad", e),
                            w="20%", placeholder_text_color=GRAY_DARK
                        ),
                        rx.input(
                            id="categoria",
                            placeholder="Categoría",
                            value=EventState.form_data["categoria"],
                            on_change=lambda e: EventState.set_form_field("categoria", e),
                            w="20%", placeholder_text_color=GRAY_DARK
                        ),
                        spacing="3", wrap="wrap", w="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.cond(
                                EventState.edit_id != None,
                                "Guardar",
                                "Agregar"
                            ),
                            type_="submit",
                            bg=RED,
                            color="white"
                        ),
                        justify="center",
                        width="100%",
                    ),
                    spacing="4",
                ),
                on_submit=EventState.process_form,
                bg="white",
                p="5",
                border_radius="10",
                w="100%",
            ),

            rx.table.root(
                rx.table.header(
                    rx.table.row(*[
                        rx.table.column_header_cell(h, color=BLUE, bg="#E0E0E0") for h in HEADERS
                    ])
                ),
                rx.table.body(rx.foreach(EventState.events, row)),
                width="100%", bg="white", border_radius="10",
            ),

            nav,

            rx.dialog.root(
                rx.dialog.trigger(rx.box()),  # invisible trigger
                rx.dialog.content(
                    rx.dialog.title("Confirmar eliminación", color="black"),
                    rx.dialog.description(
                        rx.text(
                            rx.cond(
                                EventState.delete_title != "",
                                f"¿Estás seguro que deseas eliminar el evento \"{EventState.delete_title}\"?",
                                ""
                            ),
                            color="black"
                        )
                    ),
                    rx.hstack(
                        rx.button("Cancelar", on_click=EventState.hide_modal),
                        rx.button("Aceptar", on_click=EventState.confirm_delete, bg=RED, color="white"),
                        justify="end",
                        spacing="3",
                    ),
                    bg="white",
                    padding="4",
                    border_radius="md",
                ),
                open=EventState.show_modal
            ),

            spacing="6",
            w="100%", max_w="1200px",
        ),
        position="absolute", inset="0",
        display="flex", justify_content="center", align_items="flex-start",
        bg=BG, p="6",
    )
