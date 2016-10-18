from assets.models import Asset, Asset_User_Mapping


def hello_world():
    return "Hi!"

def get_owners_and_dates(asset_ID):

    # empty object
    owners_and_dates = []
    # empty dictionary
    sort_order_of_owners = {}

    # get the asset in question
    the_asset = Asset.objects.get(pk=asset_ID)

    # extract the variables needed for later
    static_start_date = the_asset.sharing_start_date
    slot_duration = the_asset.slot_duration_unit
    num_slots = the_asset.number_of_slot_units

    # don't continue if no slots entered (will get divide by zero error)
    if num_slots == 0:
        return []

    # populate dictionary of the sort order and owners
    the_asset_mapping = Asset_User_Mapping.objects.all().filter(asset_ID=asset_ID, is_owner=True).order_by("position_in_rotation")

    if the_asset_mapping.count() == 0:
        return []

    for mapping in the_asset_mapping:

        sort_order_of_owners[mapping.position_in_rotation] = mapping.user_ID_id





    return str(sort_order_of_owners)











