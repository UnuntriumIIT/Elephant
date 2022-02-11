using Microsoft.EntityFrameworkCore.Migrations;

namespace data.Migrations
{
    public partial class searching : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "SearchWord",
                table: "Img",
                type: "text",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "SearchWord",
                table: "Img");
        }
    }
}
