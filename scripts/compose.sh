fstcompose ./fsts/L.binfst ./fsts/V_opt.binfst | fstshortestpath | fsttopsort > ./fsts/spellchecker.binfst


echo "mispelled" | fstrmepsilon | fstproject --project_output | fstcompose - ./fsts/spellchecker.binfst | fstrmepsilon | fstshortestpath | fstproject --project_output