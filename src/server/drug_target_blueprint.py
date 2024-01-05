from flask import Blueprint
from flask import request
from src.server.api_handlers.drug_target import DrugTargetApiHandler


def resolve_api_endpoints(api_handler: DrugTargetApiHandler):
    drug_target_bp = Blueprint('drug-target', __name__)

    @drug_target_bp.route('/inference', methods=['POST'])
    def inference():
        return api_handler.inference(request)
    
    @drug_target_bp.route('/add-target', methods=['POST'])
    def add_target():
        return api_handler.add_target(request)

    @drug_target_bp.route('/delete-target', methods=['POST'])
    def delete_target():
        return api_handler.delete_target(request)
    
    @drug_target_bp.route('/load-targets', methods=['GET'])
    def load_targets():
        return api_handler.load_targets(request)

    @drug_target_bp.route('/predict-3d-structure', methods=['GET'])
    def predict_3d_structure():
        return api_handler.predict_3d_structure(request)
    
    @drug_target_bp.route('/set-binding-pocket', methods=['POST'])
    def store_binding_pocket():
        return api_handler.set_binding_pocket(request)
    
    @drug_target_bp.route('/get-binding-pocket', methods=['GET'])
    def get_binding_pocket():
        return api_handler.get_binding_pocket(request)
    
    @drug_target_bp.route('/predict-binding-pocket', methods=['GET'])
    def predict_binding_pocket():
        return api_handler.predict_binding_pocket(request)
    
    @drug_target_bp.route('/add-ligand', methods=['POST'])
    def add_ligand():
        return api_handler.add_ligand(request)
    
    @drug_target_bp.route('/delete-ligand', methods=['POST'])
    def delete_ligand():
        return api_handler.delete_ligand(request)
    
    @drug_target_bp.route('/load-ligands', methods=['GET'])
    def load_ligands():
        return api_handler.load_ligands(request)

    @drug_target_bp.route('/experiments')
    def get_experiments():
        return api_handler.get_experiments()

    @drug_target_bp.route('/load-experiment', methods=['GET'])
    def get_experiment():
        return api_handler.get_experiment(request)

    @drug_target_bp.route('/load-results', methods=['GET'])
    def get_results():
        return api_handler.get_results(request)
    
    @drug_target_bp.route('/load-prediction-data', methods=['GET'])
    def get_prediction_data():
        return api_handler.get_prediction_data(request)
    
    @drug_target_bp.route('/load-experiment-progress', methods=['GET'])
    def get_experiment_progress():
        print("getting experiment progress")
        return api_handler.get_experiment_progress(request)
    
    @drug_target_bp.route('/load-experiment-instance-progress', methods=['GET'])
    def get_experiment_instance_progress():
        print("getting instance progress")
        return api_handler.get_experiment_instance_progress(request)

    @drug_target_bp.route('/delete-experiment', methods=['DELETE'])
    def delete_experiment():
        return api_handler.delete_experiment(request)

    @drug_target_bp.route('/change-experiment-name', methods=['POST'])
    def change_experiment_name():
        return api_handler.change_experiment_name(request)

    @drug_target_bp.route('/generate-id', methods=['GET'])
    def generate_id():
        return api_handler.gen_uuid()

    @drug_target_bp.route('/download-combined-pdb', methods=['POST'])
    def download_combined_pdb():
        return api_handler.download_combined_pdb(request)

    return drug_target_bp
