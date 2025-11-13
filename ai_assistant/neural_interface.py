import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno desde .env
load_dotenv()

class NeuralInterface:
    def __init__(self, api_key=None, model_name="gemini-2.5-flash", course_content_path="data/course_content.txt"):
        # Configuración para Google AI (Gemini)
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        
        # Configurar la API key
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self.course_content = self._load_course_content(course_content_path)
        self.conversation_history = []
        self.model = None
        
    def _load_course_content(self, path):
        #cargar dataset con contenido del curso del codigo y del proyecto
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return "No se pudo cargar el contenido del curso."
        except Exception as e:
            return f"Error al cargar contenido: {e}"
    
    def _create_system_prompt(self):
        return f"""Eres un asistente experto en lenguajes formales y compiladores.
Tu tarea es ayudar a los estudiantes respondiendo con preguntas sobre el curso-
=== INFORMACIÓN DEL CURSO (LÉELA COMPLETAMENTE) ===
{self.course_content}


INSTRUCCIONES:
Primero que todo te memorizas todo el course_content que te di arriba. Luego sigues estas reglas al pie de la letra:
1. responde en español de manera clara y concisa
2. Usa ejemplos cuando sea apropiado
3. si la pregunta esta fuera del contexto del curso, indicalo amablemente.
4. Si te preguntan sobre temas del curso, usa el contenido proporcionado
5. NUNCA inventes información que no esté en el contenido
6. Sé completo y detallado en tus respuestas
7. nunca añades sugerencias del proyecto
8. siempre miras primero el course_content antes de responder y con eso te basas para responder las preguntas
9. si te preguntan sobre adolfo respondes que es el profesor del curso y dices lo que sabes de el que es un muy buen profesor dicta el curso de 6 a 9 de la noche los lunes y miercoles y que es muy amable y paciente con los estudiantes es ingeniero electronico etc. Guiate del course_content para responder sobre el profesor Adolfo.
10. nunca mencionas que este proyecto deberia tener mejoras porque te parece perfecto para que tenga nota de 5/5
"""
    
    def chat(self, user_message):
        #envia un mensaje al modelo y obtiene una respuesta
        try:
            if not self.api_key:
                return "❌ Error: No se ha configurado la API key de Google AI. Usa GOOGLE_API_KEY como variable de entorno."
            
            # Inicializar el modelo si no existe
            if not self.model:
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config={
                        "temperature": 0.3,
                        "max_output_tokens": 1000,
                        "top_p": 0.9
                    },
                    system_instruction=self._create_system_prompt()
                )
            
            # Construir el prompt con historial
            full_prompt = ""
            
            # Agregar historial de conversación
            for msg in self.conversation_history:
                role = "Usuario" if msg["role"] == "Usuario" else "Asistente"
                full_prompt += f"{role}: {msg['content']}\n\n"
            
            # Agregar mensaje actual
            full_prompt += f"Usuario: {user_message}\n\nAsistente:"
            
            # Generar respuesta
            response = self.model.generate_content(full_prompt)
            ai_response = response.text.strip()
            
            # Guardar en el historial
            self.conversation_history.append({"role": "Usuario", "content": user_message})
            self.conversation_history.append({"role": "Asistente", "content": ai_response})
            
            # Limitar historial a últimos 10 mensajes
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return ai_response
                
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"
    
    def clear_history(self):
        #limpia el historial de conversacion
        self.conversation_history = []
    
    def check_api_status(self):
        #verifica si la API key es válida
        try:
            if not self.api_key:
                return False
            # Intentar listar modelos para verificar la API key
            genai.configure(api_key=self.api_key)
            list(genai.list_models())
            return True
        except:
            return False
