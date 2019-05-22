from bge import logic
from button_widget import Button
from audio import Audio
from audio_files import BUTTON_CLICK

def onHover(controller):
    hover = controller.sensors['hover']
    button = Button(controller.owner)
    
    if button.isEnabled() and hover.positive:
        hoverSound = button.getOnhoverSound()
        if hoverSound:
            Audio(hoverSound).play()

        button.applyHoverColor()
        button.runOnHoverAction()
    else:
        button.applyDefaultColor()

def onClick(controller):
    from button_effects import clickAnimation

    hover = controller.sensors['hover']
    click = controller.sensors['click']
    button = Button(controller.owner)

    if button.isEnabled() and hover.positive and click.positive:
        def onClick():
            onClickSound = button.getOnclickSound()
            if not onClickSound:
                onClickSound = BUTTON_CLICK
            Audio(onClickSound).play()
            button.runOnClickAction()

        # animate animation click and after the last frame,
        # run onclick action
        clickAnimation(button, onClick)
