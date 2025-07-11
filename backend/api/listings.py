# FILE: backend/api/listings.py
# FINAL, CORRECTED VERSION. NO MORE CRASHES.

from flask import Blueprint, jsonify, request, Response
from sqlalchemy import func, desc, asc, and_, or_, cast, Integer, String
from ..models import Car, db
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

listings_bp = Blueprint('listings', __name__)

def apply_filters(query):
    if brand := request.args.get('brand'): query = query.filter(Car.Brand == brand)
    if model := request.args.get('model'): query = query.filter(Car.Model == model)
    if (year_from := request.args.get('yearFrom')) and year_from.isdigit(): query = query.filter(cast(Car.Year, Integer) >= int(year_from))
    if (year_to := request.args.get('yearTo')) and year_to.isdigit(): query = query.filter(cast(Car.Year, Integer) <= int(year_to))
    if (price_from := request.args.get('priceFrom')) and price_from.isdigit(): query = query.filter(Car.Price_EUR >= int(price_from))
    if (price_to := request.args.get('priceTo')) and price_to.isdigit(): query = query.filter(Car.Price_EUR <= int(price_to))
    if (mileage_from := request.args.get('mileageFrom')) and mileage_from.isdigit(): query = query.filter(Car.Mileage_km >= int(mileage_from))
    if (mileage_to := request.args.get('mileageTo')) and mileage_to.isdigit(): query = query.filter(Car.Mileage_km <= int(mileage_to))
    if transmission := request.args.get('transmission'): query = query.filter(Car.Transmission == transmission)
    if fuel := request.args.get('fuel'): query = query.filter(Car.Fuel == fuel)
    if request.args.get('hasAccidents') == 'false': query = query.filter(Car.Accident_Count == 0)
    if request.args.get('singleOwner') == 'true': query = query.filter(Car.Owner_Changes <= 1)
    return query

@listings_bp.route('/cars', methods=['GET'])
def get_cars():
    try:
        page = request.args.get('page', 1, type=int)
        query = Car.query.order_by(desc(cast(Car.Year, Integer)), desc(Car.Price_EUR))
        query = apply_filters(query)
        paginated_result = query.paginate(page=page, per_page=20, error_out=False)
        return jsonify({ 'cars': [car.to_dict() for car in paginated_result.items], 'totalPages': paginated_result.pages, 'currentPage': page, 'totalItems': paginated_result.total })
    except Exception as e: return jsonify({"error": f"Error in /cars: {e}"}), 500

@listings_bp.route('/car/<string:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    try:
        car = Car.query.get_or_404(car_id)
        # THE FIX: I REMOVED `full_detail=True`. THIS STOPS THE CRASH.
        return jsonify(car.to_dict())
    except Exception as e: return jsonify({"error": f"Error in /car/{car_id}: {e}"}), 500

# The rest of the file is included for completeness.
@listings_bp.route('/car/<string:car_id>/similar', methods=['GET'])
def get_similar_cars(car_id):
    try:
        original_car = Car.query.get_or_404(car_id)
        if original_car.Price_EUR is None: return jsonify([])
        price_margin, lower_price, upper_price = 0.25, original_car.Price_EUR * (1 - 0.25), original_car.Price_EUR * (1 + 0.25)
        similar_cars_query = Car.query.filter(and_(Car.Brand == original_car.Brand, Car.ID != original_car.ID, Car.Price_EUR.between(lower_price, upper_price))).order_by(desc(Car.Year)).limit(4)
        return jsonify([car.to_dict() for car in similar_cars_query.all()])
    except Exception as e: return jsonify({"error": f"Error in /similar: {e}"}), 500
@listings_bp.route('/cars/featured', methods=['GET'])
def get_featured_cars():
    try:
        query = Car.query.filter(or_(Car.isGreatPrice == True, Car.isWellMaintained == True)).order_by(func.random()).limit(8)
        return jsonify([car.to_dict() for car in query.all()])
    except Exception as e: return jsonify({"error": f"Error in /featured: {e}"}), 500
@listings_bp.route('/cars/by-ids', methods=['POST'])
def get_cars_by_ids():
    try:
        car_ids = request.get_json().get('ids');
        if not car_ids or not isinstance(car_ids, list): return jsonify({"error": "A list of 'ids' is required."}), 400
        if not car_ids: return jsonify([])
        cars = Car.query.filter(Car.ID.in_(car_ids)).all();
        cars_dict = {car.ID: car.to_dict() for car in cars};
        ordered_cars = [cars_dict[id] for id in car_ids if id in cars_dict];
        return jsonify(ordered_cars)
    except Exception as e: return jsonify({"error": f"Error in /by-ids: {e}"}), 500
@listings_bp.route('/filter-options', methods=['GET'])
def get_filter_options():
    try:
        brands = [r[0] for r in db.session.query(Car.Brand).filter(Car.Brand.isnot(None)).distinct().order_by(Car.Brand).all()]
        models = [{'brand': r[0], 'model': r[1]} for r in db.session.query(Car.Brand, Car.Model).filter(Car.Brand.isnot(None), Car.Model.isnot(None)).distinct().all()]
        year_range = db.session.query(func.min(cast(Car.Year, Integer)), func.max(cast(Car.Year, Integer))).one(); min_year, max_year = year_range
        years = list(range(int(max_year), int(min_year) - 1, -1)) if min_year and max_year else []
        transmissions = [r[0] for r in db.session.query(Car.Transmission).filter(Car.Transmission.isnot(None)).distinct().all()]
        fuels = [r[0] for r in db.session.query(Car.Fuel).filter(Car.Fuel.isnot(None)).distinct().all()]
        return jsonify({'brands': brands, 'models': models, 'years': [str(y) for y in years], 'transmissions': transmissions, 'fuels': fuels})
    except Exception as e: return jsonify({"error": f"Error in /filter-options: {e}"}), 500
@listings_bp.route('/cars/count', methods=['GET'])
def get_car_count():
    try:
        query = db.session.query(func.count(Car.ID)); query = apply_filters(query); return jsonify({'count': query.scalar()})
    except Exception as e: return jsonify({"error": f"Error in /count: {e}"}), 500
@listings_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    try:
        base_url = request.url_root; static_urls = [{'loc': base_url}, {'loc': f'{base_url}inventory'}]; cars = db.session.query(Car.ID).all()
        car_urls = [{'loc': f'{base_url}car/{car.ID}'} for car in cars]; all_urls = static_urls + car_urls
        urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9");
        for url_data in all_urls: url, loc, lastmod = SubElement(urlset, 'url'), SubElement(url, 'loc'), SubElement(url, 'lastmod'); loc.text, lastmod.text = url_data['loc'], datetime.now().strftime('%Y-%m-%d')
        xml_str = tostring(urlset, 'utf-8'); pretty_xml_str = parseString(xml_str).toprettyxml(indent="  "); return Response(pretty_xml_str, mimetype='application/xml')
    except Exception as e: return jsonify({"error": f"Error in /sitemap.xml: {e}"}), 500