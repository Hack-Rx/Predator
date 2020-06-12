from nutritionix import Nutritionix
nix = Nutritionix(app_id="a43c505b", api_key="ce2e2ad8e38bbf9dbb2043575c591179")
a=nix.search("pizza", results="0:1").json()
b=a['hits']
_id=b[0]
food_calorie=nix.item(id=_id['_id']).json()['nf_calories']
