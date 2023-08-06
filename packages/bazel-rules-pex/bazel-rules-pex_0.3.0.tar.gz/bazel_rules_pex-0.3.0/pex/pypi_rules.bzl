
def _pypi_wheel_impl(repository_ctx):
  """asdf"""

  repository_ctx.execute([
      "pip", "download", repository_ctx.attr.req,
  ])

  repository_ctx.file(
      "BUILD",
      "\n".join([
          "filegroup(name = 'file',",
          "          srcs = glob(['**']))"
      ]))


pypi_package = repository_rule(
  _pypi_wheel_impl,
  attrs = {"req": attr.string(mandatory=True)},
)
