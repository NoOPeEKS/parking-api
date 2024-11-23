from fastapi import APIRouter

router = APIRouter(prefix="/parking")


@router.get(path="/{parking_id}")
def get_parking_info(parking_id: int):
    print(parking_id)
    return {"message": "recieved parking id"}
