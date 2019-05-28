from canvas import Canvas

class NotificationCanvas(Canvas):
    def __init__(self, sceneId='HUD'):
        super(NotificationCanvas, self).__init__(
            'notification_canvas', 'notification_canvas', sceneId
        )

    @property
    def infoTxtObj(self):
        return self._getWidget('txt_notification_info')
