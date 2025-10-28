import requests
import json
import os

class NeuralInterface:
    def __init__(self, model_name="llama3:latest", course_content_path="data/course_content.txt"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        self.course_content = self._load_course_content(course_content_path)
        self.conversation_history = []
        
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
1. responde en español de manera clara y concisa
2. Usa ejemplos cuando sea apropiado
3. si la pregunta esta fuera del contexto del curso, indicalo amablemente.
4. Si te preguntan sobre temas del curso, usa el contenido proporcionado
5. NUNCA inventes información que no esté en el contenido
6. Sé completo y detallado en tus respuestas
7. nunca añades sugerencias del proyecto
"""
    
    def chat(self, user_message):
        #envia un mensaje al modelo y obtiene una respuesta
        try:
            # Construir el prompt completo
            if not self.conversation_history:
                full_prompt = f"{self._create_system_prompt()}\n\nUsuario: {user_message}\nAsistente:"
            else:
                # Incluir historial de conversación
                history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
                full_prompt = f"{self._create_system_prompt()}\n\n{history}\nUsuario: {user_message}\nAsistente:"
            
            # Preparar el payload para Ollama
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Más determinista, menos creativo
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            # Hacer la petición a Ollama
            response = requests.post(self.api_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '').strip()
                
                # Guardar en el historial
                self.conversation_history.append({"role": "Usuario", "content": user_message})
                self.conversation_history.append({"role": "Asistente", "content": ai_response})
                
                # Limitar historial a últimos 10 mensajes
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
                
                return ai_response
            else:
                return f"Error: No se pudo conectar con Ollama (código {response.status_code})"
                
        except requests.exceptions.ConnectionError:
            return "❌ Error: No se pudo conectar con Ollama. Asegúrate de que Ollama esté ejecutándose."
        except requests.exceptions.Timeout:
            return "⏱️ Error: La solicitud ha excedido el tiempo de espera."
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"
    
    def clear_history(self):
        #limpia el historial de conversacion
        self.conversation_history = []
    
    def check_ollama_status(self):
        #verifica si ollama esta corriendo
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
