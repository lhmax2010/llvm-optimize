import json
from pathlib import Path
from validate import E,V,INNER,BUILD,root,run,save
p=V/'plugin-smoke.c';p.write_text('#pragma enable_annotate\nvoid example(void) {}\n')
buildlines=(E/'build-metadata/build.ninja').read_text().splitlines();i=next(i for i,s in enumerate(buildlines) if s.startswith('build lib64/AnnotateFunctions.so:'));(E/'annotate-link-edge.txt').write_text('\n'.join(f'{n+1}: {buildlines[n]}' for n in range(i,i+12))+'\n')
run('annotate-dynsym',['readelf','--dyn-syms','-W',str(BUILD/'lib64/AnnotateFunctions.so')])
r=root('annotate-plugin-smoke-corrected',['/usr/bin/clang','--no-default-config','-Xclang','-load','-Xclang','/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/AnnotateFunctions.so','-Xclang','-ast-dump','-fsyntax-only',INNER+'/plugin-smoke.c'],60)
save('annotate-analysis.json',{'frozen_expectation':'libLLVM NEEDED','actual_needed':['libstdc++.so.6','libc.so.6'],'link_flags_include_as_needed':True,'link_libraries_include_libLLVM':True,'plugin_run_rc':r['rc'],'annotation_observed':'example_annotation' in r['stdout'],'initial_probe_error':'--no-default-config before -cc1 selects driver; corrected to -Xclang forwarding, initial argv/stderr retained','interpretation':'Consistent with --as-needed dropping an unused DSO dependency; no relink counterfactual was performed. Frozen-table ANALYSIS_PENDING is retained.'})
