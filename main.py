"""
Ponto de entrada da aplicação Synapse.
Configura e inicializa o servidor Flask com todos os serviços e rotas.
"""

from flask import Flask, jsonify, render_template, session, redirect, request, url_for
from functools import wraps
from synapse.services.seed_loader import SeedLoader
from synapse.repositories.implementations.inmemory_patient_repository import InMemoryPatientRepository
from synapse.repositories.implementations.inmemory_psychologist_repository import InMemoryPsychologistRepository
from synapse.repositories.implementations.inmemory_appointment_repository import InMemoryAppointmentRepository
from synapse.repositories.implementations.inmemory_user_repository import InMemoryUserRepository
from synapse.repositories.implementations.inmemory_clinic_repository import InMemoryClinicRepository
from synapse.repositories.implementations.inmemory_lead_repository import InMemoryLeadRepository
from synapse.repositories.implementations.inmemory_availability_repository import InMemoryAvailabilityRepository

# Services
from synapse.services.auth_service import AuthService
from synapse.services.patient_service import PatientService
from synapse.services.psychologist_service import PsychologistService
from synapse.services.appointment_service import AppointmentService
from synapse.services.clinic_service import ClinicService
from synapse.services.lead_service import LeadService
from synapse.services.availability_service import AvailabilityService

# Controllers
from synapse.controllers.auth_controller import create_auth_routes
from synapse.controllers.patient_controller import create_patient_routes
from synapse.controllers.psychologist_controller import create_psychologist_routes
from synapse.controllers.appointment_controller import create_appointment_routes
from synapse.controllers.clinic_controller import create_clinic_routes
from synapse.controllers.lead_controller import create_lead_routes
from synapse.controllers.availability_controller import create_availability_routes

from synapse.api.response import ApiResponse


def login_required(user_type=None):
    """
    Decorator que protege rotas exigindo autenticação via session.
    
    Args:
        user_type: Tipo de usuário permitido ('patient', 'psychologist', 'clinic') ou None para qualquer
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                # Redireciona para login apropriado
                if user_type == 'psychologist':
                    return redirect(url_for('psychologist_login'))
                elif user_type == 'clinic':
                    return redirect(url_for('clinic_login'))
                else:
                    return redirect(url_for('patient_login'))
            
            # Verifica tipo de usuário se especificado
            if user_type and session.get('user_type') != user_type:
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def create_app():
    """
    Factory function para criar e configurar a aplicação Flask.
    
    Returns:
        Flask: Aplicação configurada
    """
    app = Flask(__name__, 
                template_folder='synapse/views/templates',
                static_folder='synapse/views/static',
                static_url_path='/static')
    
    app.secret_key = 'synapse-dev-secret-key-2025'

    # =========================================================================
    # INICIALIZAÇÃO DOS REPOSITÓRIOS
    # =========================================================================
    data = SeedLoader.load()
    
    patient_repo = InMemoryPatientRepository(data['patients'])
    psychologist_repo = InMemoryPsychologistRepository(data['psychologists'])
    availability_repo = InMemoryAvailabilityRepository(data['availabilities'])
    appointment_repo = InMemoryAppointmentRepository(data['appointments'])
    user_repo = InMemoryUserRepository(data['users'])
    clinic_repo = InMemoryClinicRepository(data['clinics'])
    lead_repo = InMemoryLeadRepository(data['leads'])

    # =========================================================================
    # INICIALIZAÇÃO DOS SERVIÇOS
    # =========================================================================
    auth_service = AuthService(user_repo)
    patient_service = PatientService(patient_repo)
    psychologist_service = PsychologistService(psychologist_repo)
    clinic_service = ClinicService(clinic_repo)
    lead_service = LeadService(lead_repo)
    
    availability_service = AvailabilityService(availability_repo, psychologist_repo)
    
    appointment_service = AppointmentService(
        appointment_repo, patient_repo, psychologist_repo, availability_repo
    )

    # =========================================================================
    # REGISTRO DOS BLUEPRINTS (ROTAS DA API)
    # =========================================================================
    app.register_blueprint(create_auth_routes(auth_service))
    app.register_blueprint(create_patient_routes(patient_service))
    app.register_blueprint(create_psychologist_routes(psychologist_service))
    app.register_blueprint(create_appointment_routes(appointment_service))
    app.register_blueprint(create_clinic_routes(clinic_service))
    app.register_blueprint(create_lead_routes(lead_service))
    app.register_blueprint(create_availability_routes(availability_service))

    # =========================================================================
    # ROTAS DE VIEWS (FRONTEND)
    # =========================================================================
    @app.route("/", methods=["GET"])
    def index():
        """Página inicial."""
        return render_template('index.html')

    @app.route("/patient/login", methods=["GET"])
    def patient_login():
        """Página de login do paciente."""
        if 'user_id' in session and session.get('user_type') == 'patient':
            return redirect(url_for('patient_booking'))
        return render_template('patient_login.html')

    @app.route("/patient/booking", methods=["GET"])
    @login_required(user_type='patient')
    def patient_booking():
        """Página de agendamento do paciente - requer login."""
        return render_template('patient_booking.html')

    @app.route("/psychologist/login", methods=["GET"])
    def psychologist_login():
        """Página de login do psicólogo."""
        if 'user_id' in session and session.get('user_type') == 'psychologist':
            return redirect(url_for('psychologist_dashboard'))
        return render_template('psychologist_login.html')

    @app.route("/psychologist/dashboard", methods=["GET"])
    @login_required(user_type='psychologist')
    def psychologist_dashboard():
        """Dashboard do psicólogo - requer login."""
        return render_template('psychologist_dashboard.html')

    @app.route("/clinic/login", methods=["GET"])
    def clinic_login():
        """Página de login da clínica."""
        if 'user_id' in session and session.get('user_type') == 'clinic':
            return redirect(url_for('clinic_dashboard'))
        return render_template('clinic_login.html')

    @app.route("/clinic/dashboard", methods=["GET"])
    @login_required(user_type='clinic')
    def clinic_dashboard():
        """Dashboard da clínica - requer login."""
        return render_template('clinic_dashboard.html')

    @app.route("/auth/login", methods=["POST"])
    def do_login():
        """Processa login via formulário e cria session."""
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'patient')
        
        try:
            # O método login() retorna um objeto User, não um dicionário
            user = auth_service.login(email, password)
            
            if user:
                session['user_id'] = user.id
                session['user_name'] = user.name if user.name else email.split('@')[0]
                session['user_email'] = email
                session['user_type'] = user.user_type if hasattr(user, 'user_type') else user_type
                
                # Redirecionar baseado no tipo
                if session['user_type'] == 'psychologist':
                    return redirect(url_for('psychologist_dashboard'))
                elif session['user_type'] == 'clinic':
                    return redirect(url_for('clinic_dashboard'))
                else:
                    return redirect(url_for('patient_booking'))
            else:
                # Falha no login - voltar com mensagem
                from flask import flash
                flash('Email ou senha inválidos', 'error')
                if user_type == 'psychologist':
                    return redirect(url_for('psychologist_login'))
                elif user_type == 'clinic':
                    return redirect(url_for('clinic_login'))
                else:
                    return redirect(url_for('patient_login'))
                    
        except Exception as e:
            from flask import flash
            flash(f'Erro ao fazer login: {str(e)}', 'error')
            return redirect(url_for('index'))

    @app.route("/auth/logout", methods=["GET"])
    def logout():
        """Encerra a session do usuário."""
        session.clear()
        return redirect(url_for('index'))

    # =========================================================================
    # ROTA DE HEALTH CHECK
    # =========================================================================
    @app.route("/health", methods=["GET"])
    def health_check():
        """
        Endpoint de verificação de saúde da API.
        
        Returns:
            JSON com status da aplicação
        """
        return ApiResponse.success({
            "status": "healthy",
            "service": "Synapse API",
            "version": "1.0.0"
        })

    return app


# Criar instância da aplicação
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
