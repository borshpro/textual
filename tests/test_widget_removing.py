import asyncio
from textual.app import App
from textual.widget import Widget
from textual.widgets import Static, Button
from textual.containers import Container

async def await_remove_standin():
    """Standin function for awaiting removal.

    These tests are being written so that we can go on and make remove
    awaitable, but it would be good to have some tests in place *before* we
    make that change, but the tests need to await remove to be useful tests.
    So to get around that bootstrap issue, we just use this function as a
    standin until we can swap over.
    """
    await asyncio.sleep(0) # Until we can await remove.

async def test_remove_single_widget():
    """It should be possible to the only widget on a screen."""
    async with App().run_test() as pilot:
        await pilot.app.mount(Static())
        assert len(pilot.app.screen.children) == 1
        pilot.app.query_one(Static).remove()
        await await_remove_standin()
        assert len(pilot.app.screen.children) == 0

async def test_many_remove_all_widgets():
    """It should be possible to remove all widgets on a multi-widget screen."""
    async with App().run_test() as pilot:
        await pilot.app.mount(*[Static() for _ in range(1000)])
        assert len(pilot.app.screen.children) == 1000
        pilot.app.query(Static).remove()
        await await_remove_standin()
        assert len(pilot.app.screen.children) == 0

async def test_many_remove_some_widgets():
    """It should be possible to remove some widgets on a multi-widget screen."""
    async with App().run_test() as pilot:
        await pilot.app.mount(*[Static(id=f"is-{n%2}") for n in range(1000)])
        assert len(pilot.app.screen.children) == 1000
        pilot.app.query("#is-0").remove()
        await await_remove_standin()
        assert len(pilot.app.screen.children) == 500

async def test_remove_branch():
    """It should be possible to remove a whole branch in the DOM."""
    async with App().run_test() as pilot:
        await pilot.app.mount(
            Container(
                Container(
                    Container(
                        Container(
                            Container(
                                Static()
                            )
                        )
                    )
                )
            ),
            Static(),
            Container(
                Container(
                    Container(
                        Container(
                            Container(
                                Static()
                            )
                        )
                    )
                )
            ),
        )
        assert len(pilot.app.screen.walk_children(with_self=False)) == 13
        pilot.app.screen.children[0].remove()
        await await_remove_standin()
        assert len(pilot.app.screen.walk_children(with_self=False)) == 7

async def test_remove_overlap():
    """It should be possible to remove an overlapping collection of widgets."""
    async with App().run_test() as pilot:
        await pilot.app.mount(
            Container(
                Container(
                    Container(
                        Container(
                            Container(
                                Static()
                            )
                        )
                    )
                )
            ),
            Static(),
            Container(
                Container(
                    Container(
                        Container(
                            Container(
                                Static()
                            )
                        )
                    )
                )
            ),
        )
        assert len(pilot.app.screen.walk_children(with_self=False)) == 13
        pilot.app.query(Container).remove()
        await await_remove_standin()
        assert len(pilot.app.screen.walk_children(with_self=False)) == 1

async def test_remove_move_focus():
    """Removing a focused widget should settle focus elsewhere."""
    async with App().run_test() as pilot:
        buttons = [ Button(str(n)) for n in range(10)]
        await pilot.app.mount(Container(*buttons[:5]), Container(*buttons[5:]))
        assert len(pilot.app.screen.children) == 2
        assert len(pilot.app.screen.walk_children(with_self=False)) == 12
        assert pilot.app.focused is None
        await pilot.press( "tab" )
        assert pilot.app.focused is not None
        assert pilot.app.focused == buttons[0]
        pilot.app.screen.children[0].remove()
        await await_remove_standin()
        assert len(pilot.app.screen.children) == 1
        assert len(pilot.app.screen.walk_children(with_self=False)) == 6
        assert pilot.app.focused is not None
        assert pilot.app.focused == buttons[9]