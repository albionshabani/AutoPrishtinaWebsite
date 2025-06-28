from flask import Blueprint, jsonify, request
from sqlalchemy import func
from ..models.car import Car
from .. import db

listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/api/listings', methods=['GET'])
def get_listings():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        sort_by = request.args.get('sort_by', 'ID')
        order = request.args.get('order', 'asc')

        # --- Basic Validation ---
        allowed_sort_columns = [
            'ID', 'Year', 'Brand', 'Model', 'Badge', 'Mileage_km',
            'Price_KRW', 'Price_EUR', 'Fuel', 'Transmission',
            'First_Registration_Date', 'Displacement_cc'
        ]
        if sort_by not in allowed_sort_columns:
            sort_by = 'ID'
            
        sort_column = getattr(Car, sort_by)
        sort_order = sort_column.desc() if order == 'desc' else sort_column.asc()

        # --- Filtering ---
        query = Car.query

        filters = {
            'brand': request.args.get('brand'),
            'model': request.args.get('model'),
            'fuel': request.args.get('fuel'),
            'transmission': request.args.get('transmission'),
            'year_min': request.args.get('year_min', type=int),
            'year_max': request.args.get('year_max', type=int),
            'price_min': request.args.get('price_min', type=int),
            'price_max': request.args.get('price_max', type=int),
            'mileage_min': request.args.get('mileage_min', type=int),
            'mileage_max': request.args.get('mileage_max', type=int),
        }

        if filters['brand']:
            query = query.filter(Car.Brand.ilike(f"%{filters['brand']}%"))
        if filters['model']:
            query = query.filter(Car.Model.ilike(f"%{filters['model']}%"))
        if filters['fuel']:
            query = query.filter(Car.Fuel == filters['fuel'])
        if filters['transmission']:
            query = query.filter(Car.Transmission == filters['transmission'])
        if filters['year_min']:
            query = query.filter(Car.Year >= filters['year_min'])
        if filters['year_max']:
            query = query.filter(Car.Year <= filters['year_max'])
        if filters['price_min']:
            query = query.filter(Car.Price_EUR >= filters['price_min'])
        if filters['price_max']:
            query = query.filter(Car.Price_EUR <= filters['price_max'])
        if filters['mileage_min']:
            query = query.filter(Car.Mileage_km >= filters['mileage_min'])
        if filters['mileage_max']:
            query = query.filter(Car.Mileage_km <= filters['mileage_max'])

        # --- Execute Query ---
        total_count = query.count()
        paginated_query = query.order_by(sort_order).paginate(page=page, per_page=per_page, error_out=False)
        cars = paginated_query.items
        
        car_list = [car.to_dict() for car in cars]
        
        return jsonify({
            "listings": car_list,
            "page": page,
            "perPage": per_page,
            "totalCount": total_count,
            "totalPages": paginated_query.pages
        })
        
    except Exception as e:
        print(f"API Error fetching listings: {e}")
        return jsonify({"error": "An error occurred while fetching listings."}), 500

@listings_bp.route('/api/filter-options', methods=['GET'])
def get_filter_options():
    try:
        brands = [r[0] for r in db.session.query(Car.Brand).distinct().order_by(Car.Brand).all() if r[0]]
        models = [r[0] for r in db.session.query(Car.Model).distinct().order_by(Car.Model).all() if r[0]]
        fuels = [r[0] for r in db.session.query(Car.Fuel).distinct().order_by(Car.Fuel).all() if r[0]]
        transmissions = [r[0] for r in db.session.query(Car.Transmission).distinct().order_by(Car.Transmission).all() if r[0]]

        return jsonify({
            'brands': brands,
            'models': models,
            'fuels': fuels,
            'transmissions': transmissions
        })
    except Exception as e:
        print(f"API Error fetching filter options: {e}")
        return jsonify({"error": "Could not retrieve filter options."}), 500

@listings_bp.route('/api/listings/<string:car_id>', methods=['GET'])
def get_listing_by_id(car_id):
    """Fetches a single car by its ID."""
    try:
        car = Car.query.get(car_id)
        if car is None:
            return jsonify({"error": "Listing not found"}), 404
        
        return jsonify(car.to_dict())
        
    except Exception as e:
        print(f"API Error fetching single listing: {e}")
        return jsonify({"error": "An error occurred."}), 500
