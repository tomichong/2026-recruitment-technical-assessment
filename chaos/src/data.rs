use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // Calculate sums and return response

    // I LOVE RUST! TAKE 6991 IF YOU HAVENT!

    let mut string_len = 0;
    let mut int_sum = 0;

    for d in request.data.iter() {
        match d {
            Element::Num(num) => {
                int_sum += num;
            },
            Element::Text(text) => {
                string_len += text.len();
            },
        }
    }

    let response = DataResponse {
        string_len: string_len,
        int_sum: int_sum,
    };

    (StatusCode::OK, Json(response))
}

// since multiple data types can exist in the same list
#[derive(Deserialize)]
#[serde(untagged)]
enum Element {
    // i assume that numbers can only be ints as the response has the key int_sum
    Num(i32),
    // i assume that text can only be strings as the response has the key string_len
    Text(String)
}

#[derive(Deserialize)]
pub struct DataRequest {
    // Add any fields here
    data: Vec<Element>
}

#[derive(Serialize)]
pub struct DataResponse {
    // Add any fields here
    string_len: usize,
    int_sum: i32
}
