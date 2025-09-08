from django.apps import AppConfig

class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mainpage'

    def ready(self):
        print("🚀 AppConfig ready running...")
        
        try:
            import Mainpage.signals
            print("📡 Signals successfully imported")
        except Exception as e:
            print("❌ Failed to import signals:", e)




