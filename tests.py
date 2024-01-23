def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_slug": "test_project"})
    assert result.exit_code == 0
