### Summary

Resolve #Issue

### Other Information

If there's anything else that's important and relevant to your pull
request, mention that information here. This could include
benchmarks, or other information.

If you are updating any of the CHANGELOG files or are asked to update the
CHANGELOG files by reviewers, please add the CHANGELOG entry at the top of the file.

Thanks for contributing to `gfzs` !


### Work

Please write the operation check method.


### Test

Currently there are no tests.  
Instead, the operation is guaranteed by executing the following command and actually checking the operation.

- [ ] python3 gfzs/views/not_found.py
- [ ] python3 gfzs/views/paging.py
- [ ] python3 gfzs/views/footer.py
- [ ] python3 gfzs/views/header.py
- [ ] python3 gfzs/views/search_result.py
- [ ] python3 gfzs/utils/markup.py
- [ ] python3 gfzs/utils/color.py
- [ ] python3 gfzs/config/app.py
- [ ] python3 gfzs/cmd/init.py
- [ ] python3 gfzs/cmd/edit.py
- [ ] python3 gfzs/cmd/demo.py
- [ ] python3 gfzs/cmd/valid.py
- [ ] python3 gfzs/controller.py
- [ ] python3 gfzs/model.py
- [ ] cat fixtures/rust.json | bin/gfzs -s 20
- [ ] cat fixtures/rust.json | python3 -m gfzs -s 40
- [ ] bin/gfzs init
- [ ] bin/gfzs edit
- [ ] bin/gfzs demo
- [ ] bin/gfzs valid
- [ ] black gfzs/**/*.py
