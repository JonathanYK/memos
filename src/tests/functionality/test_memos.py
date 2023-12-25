
def test_memo_id_generator_page(test_client, return_memo_id=False):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/memo_id' page is requested (GET)
    THEN check that a valid memo id generated.
    """

    response = test_client.get('/memo_id')
    ret_lst = str(response.data)[2:-1].split(":")
    gen_memo_id = int(ret_lst[1][1:])

    assert ret_lst[0] == "Memo ID generated"
    
    # gen_memo_id has to be exactly 9 digits:
    assert len(str(gen_memo_id)) == 9
    assert response.status_code == 201

    if return_memo_id:
        return gen_memo_id

