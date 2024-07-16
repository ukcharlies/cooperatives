from bs4 import BeautifulSoup
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUser
from .models import UserProfile, User
from .serializers import UserRegistrationSerializer, LoginSerializer


@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"access": access_token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"access": access_token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsSuperUser])
def unverified_users(request):
    # Get all users whose UserProfile.is_verified is False
    unverified_profiles = UserProfile.objects.filter(is_verified=False)

    # Create a list of dictionaries with the required fields
    unverified_users_list = []
    for profile in unverified_profiles:
        user = profile.user
        user_data = {
            "id": user.id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "department": profile.department.name if profile.department else None,
            "employmentNumber": profile.employment_number,
            "address": profile.address,
            "phoneNumber": profile.phone,
            "email": user.email,
        }
        unverified_users_list.append(user_data)

    # Return the list as a JSON response
    return Response(unverified_users_list, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsSuperUser])
def verify_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        return Response(
            {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
        )
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "UserProfile does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    user_profile.is_verified = True
    user_profile.save()

    return Response(
        {"message": "User verified successfully."}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "UserProfile does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    if not user_profile.is_verified:
        return Response({"message": "awaiting verification"}, status=status.HTTP_200_OK)

    user_data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "department": user_profile.department.name if user_profile.department else None,
        "address": user_profile.address,
        "phone": user_profile.phone,
        "employment_number": user_profile.employment_number,
        "is_verified": user_profile.is_verified,
        "is_superuser": user.is_superuser,  # Add this line to include superuser status
    }
    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_news_events(request):
    url = "https://augustineuniversity.edu.ng/News_Events"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Referer": "https://augustineuniversity.edu.ng/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return Response(
            {"error": "Failed to fetch news."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the specific div elements
    target_section = soup.select_one(
        "section > .container.mt-30.mb-30.pt-30.pb-30 > .row > .col-md-9 > .blog-posts.single-post"
    )
    data_list = []

    if target_section:
        divs = target_section.find_all(
            "div", class_="col-xs-12 col-sm-6 col-md-6 mb-30 wow fadeInRight"
        )

        for div in divs:
            title_tag = div.find("h4").find("a")
            img_tag = div.find("img")
            date_tag = div.find("li", class_="pr-0")
            location_tag = div.find("li", class_="pl-5")

            title = title_tag.text.strip()
            img_url = "https://augustineuniversity.edu.ng/" + img_tag["src"]
            href = "https://augustineuniversity.edu.ng/" + title_tag["href"]
            date = date_tag.text.strip().replace("|", "").strip()
            location = location_tag.text.strip()

            desc = f"{location}, {date}"

            data_list.append(
                {"title": title, "thumbnail": img_url, "href": href, "desc": desc}
            )

        return Response(data_list, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Failed to fetch news."},
            status=status.HTTP_404_NOT_FOUND,
        )
