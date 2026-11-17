#include "clang/AST/ASTConsumer.h"
#include "clang/AST/Decl.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Frontend/FrontendPluginRegistry.h"
#include "llvm/Support/raw_ostream.h"
using namespace clang;
class NamesConsumer : public ASTConsumer {
 public:
  bool HandleTopLevelDecl(DeclGroupRef group) override {
    for (Decl *decl : group)
      if (auto *fn = llvm::dyn_cast<FunctionDecl>(decl))
        llvm::errs() << "PLUGIN_FUNCTION " << fn->getNameAsString() << "\n";
    return true;
  }
};
class NamesAction : public PluginASTAction {
  std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &, llvm::StringRef) override {
    return std::make_unique<NamesConsumer>();
  }
  bool ParseArgs(const CompilerInstance &, const std::vector<std::string> &) override { return true; }
  ActionType getActionType() override { return AddBeforeMainAction; }
};
static FrontendPluginRegistry::Add<NamesAction> X("names", "print top-level functions");
