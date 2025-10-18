using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

#nullable disable

namespace Innts.Migrations
{
    /// <inheritdoc />
    public partial class test : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "AspNetRoles",
                columns: table => new
                {
                    Id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    Name = table.Column<string>(type: "character varying(256)", maxLength: 256, nullable: true),
                    NormalizedName = table.Column<string>(type: "character varying(256)", maxLength: 256, nullable: true),
                    ConcurrencyStamp = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetRoles", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "AspNetUsers",
                columns: table => new
                {
                    Id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    FirstName = table.Column<string>(type: "text", nullable: false),
                    LastName = table.Column<string>(type: "text", nullable: false),
                    IsActivate = table.Column<bool>(type: "boolean", nullable: false),
                    PasswordHash = table.Column<string>(type: "text", nullable: false),
                    PhoneNumber = table.Column<string>(type: "text", nullable: true),
                    EmailConfirmed = table.Column<bool>(type: "boolean", nullable: false),
                    AccessFailedCount = table.Column<int>(type: "integer", nullable: false),
                    NormalizedEmail = table.Column<string>(type: "character varying(256)", maxLength: 256, nullable: false),
                    NormalizedUserName = table.Column<string>(type: "character varying(256)", maxLength: 256, nullable: false),
                    SecurityStamp = table.Column<string>(type: "text", nullable: false),
                    ConcurrencyStamp = table.Column<string>(type: "text", nullable: false),
                    PhoneNumberConfirmed = table.Column<bool>(type: "boolean", nullable: false),
                    TwoFactorEnabled = table.Column<bool>(type: "boolean", nullable: false),
                    LockoutEnabled = table.Column<bool>(type: "boolean", nullable: false),
                    KbDatabaseChache = table.Column<List<string>>(type: "text[]", nullable: true),
                    UserName = table.Column<string>(type: "character varying(256)", maxLength: 256, nullable: true),
                    Email = table.Column<string>(type: "character varying(256)", maxLength: 256, nullable: true),
                    LockoutEnd = table.Column<DateTimeOffset>(type: "timestamp with time zone", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUsers", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Companies",
                columns: table => new
                {
                    Id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    inn = table.Column<string>(type: "text", nullable: false),
                    orgName = table.Column<string>(type: "text", nullable: false),
                    orgFullName = table.Column<string>(type: "text", nullable: false),
                    status = table.Column<string>(type: "text", nullable: false),
                    legalAddress = table.Column<string>(type: "text", nullable: false),
                    productionAddress = table.Column<string>(type: "text", nullable: false),
                    director = table.Column<string>(type: "text", nullable: false),
                    okved_description = table.Column<string>(type: "text", nullable: false),
                    additionalSiteAddress = table.Column<string>(type: "text", nullable: false),
                    industry = table.Column<string>(type: "text", nullable: false),
                    subIndustry = table.Column<string>(type: "text", nullable: false),
                    mainOkved = table.Column<string>(type: "text", nullable: false),
                    mainOkvedActivity = table.Column<string>(type: "text", nullable: false),
                    productionOkved = table.Column<string>(type: "text", nullable: false),
                    registrationDate = table.Column<string>(type: "text", nullable: false),
                    head = table.Column<string>(type: "text", nullable: false),
                    parentOrgName = table.Column<string>(type: "text", nullable: false),
                    parentOrgInn = table.Column<int>(type: "integer", nullable: false),
                    managementContacts = table.Column<string>(type: "text", nullable: false),
                    orgContact = table.Column<string>(type: "text", nullable: false),
                    emergencyContact = table.Column<string>(type: "text", nullable: false),
                    website = table.Column<string>(type: "text", nullable: false),
                    email = table.Column<string>(type: "text", nullable: false),
                    supportMeasures = table.Column<string>(type: "text", nullable: false),
                    specialStatus = table.Column<string>(type: "text", nullable: false),
                    smeStatus = table.Column<string>(type: "text", nullable: false),
                    revenue2022 = table.Column<int>(type: "integer", nullable: false),
                    revenue2023 = table.Column<int>(type: "integer", nullable: false),
                    revenue2024 = table.Column<int>(type: "integer", nullable: false),
                    profit2022 = table.Column<int>(type: "integer", nullable: false),
                    profit2023 = table.Column<int>(type: "integer", nullable: false),
                    profit2024 = table.Column<int>(type: "integer", nullable: false),
                    staffTotal2022 = table.Column<int>(type: "integer", nullable: false),
                    staffTotal2023 = table.Column<int>(type: "integer", nullable: false),
                    staffTotal2024 = table.Column<int>(type: "integer", nullable: false),
                    staffMoscow2022 = table.Column<int>(type: "integer", nullable: false),
                    staffMoscow2023 = table.Column<int>(type: "integer", nullable: false),
                    staffMoscow2024 = table.Column<int>(type: "integer", nullable: false),
                    payrollTotal2022 = table.Column<int>(type: "integer", nullable: false),
                    payrollTotal2023 = table.Column<int>(type: "integer", nullable: false),
                    payrollTotal2024 = table.Column<int>(type: "integer", nullable: false),
                    payrollMoscow2022 = table.Column<int>(type: "integer", nullable: false),
                    payrollMoscow2023 = table.Column<int>(type: "integer", nullable: false),
                    payrollMoscow2024 = table.Column<int>(type: "integer", nullable: false),
                    avgSalaryTotal2022 = table.Column<int>(type: "integer", nullable: false),
                    avgSalaryTotal2023 = table.Column<int>(type: "integer", nullable: false),
                    avgSalaryTotal2024 = table.Column<int>(type: "integer", nullable: false),
                    avgSalaryMoscow2022 = table.Column<int>(type: "integer", nullable: false),
                    avgSalaryMoscow2023 = table.Column<int>(type: "integer", nullable: false),
                    avgSalaryMoscow2024 = table.Column<int>(type: "integer", nullable: false),
                    taxTotal2022 = table.Column<int>(type: "integer", nullable: false),
                    taxTotal2023 = table.Column<int>(type: "integer", nullable: false),
                    taxTotal2024 = table.Column<int>(type: "integer", nullable: false),
                    taxProfit2022 = table.Column<int>(type: "integer", nullable: false),
                    taxProfit2023 = table.Column<int>(type: "integer", nullable: false),
                    taxProfit2024 = table.Column<int>(type: "integer", nullable: false),
                    taxProperty2022 = table.Column<int>(type: "integer", nullable: false),
                    taxProperty2023 = table.Column<int>(type: "integer", nullable: false),
                    taxProperty2024 = table.Column<int>(type: "integer", nullable: false),
                    taxLand2022 = table.Column<int>(type: "integer", nullable: false),
                    taxLand2023 = table.Column<int>(type: "integer", nullable: false),
                    taxLand2024 = table.Column<int>(type: "integer", nullable: false),
                    taxNdfl2022 = table.Column<int>(type: "integer", nullable: false),
                    taxNdfl2023 = table.Column<int>(type: "integer", nullable: false),
                    taxNdfl2024 = table.Column<int>(type: "integer", nullable: false),
                    taxTransport2022 = table.Column<int>(type: "integer", nullable: false),
                    taxTransport2023 = table.Column<int>(type: "integer", nullable: false),
                    taxTransport2024 = table.Column<int>(type: "integer", nullable: false),
                    taxOther2022 = table.Column<int>(type: "integer", nullable: false),
                    taxOther2023 = table.Column<int>(type: "integer", nullable: false),
                    taxOther2024 = table.Column<int>(type: "integer", nullable: false),
                    excise2022 = table.Column<int>(type: "integer", nullable: false),
                    excise2023 = table.Column<int>(type: "integer", nullable: false),
                    excise2024 = table.Column<int>(type: "integer", nullable: false),
                    investMoscow2022 = table.Column<int>(type: "integer", nullable: false),
                    investMoscow2023 = table.Column<int>(type: "integer", nullable: false),
                    investMoscow2024 = table.Column<int>(type: "integer", nullable: false),
                    export2022 = table.Column<int>(type: "integer", nullable: false),
                    export2023 = table.Column<int>(type: "integer", nullable: false),
                    export2024 = table.Column<int>(type: "integer", nullable: false),
                    landCadastral = table.Column<string>(type: "text", nullable: false),
                    landArea = table.Column<int>(type: "integer", nullable: false),
                    landUse = table.Column<string>(type: "text", nullable: false),
                    landOwnership = table.Column<string>(type: "text", nullable: false),
                    landOwner = table.Column<string>(type: "text", nullable: false),
                    oksCadastral = table.Column<string>(type: "text", nullable: false),
                    oksArea = table.Column<int>(type: "integer", nullable: false),
                    oksUse = table.Column<string>(type: "text", nullable: false),
                    oksType = table.Column<string>(type: "text", nullable: false),
                    oksOwnership = table.Column<string>(type: "text", nullable: false),
                    oksOwner = table.Column<string>(type: "text", nullable: false),
                    productionArea = table.Column<int>(type: "integer", nullable: false),
                    standardizedProduct = table.Column<string>(type: "text", nullable: false),
                    productNames = table.Column<string>(type: "text", nullable: false),
                    productOkpd2 = table.Column<string>(type: "text", nullable: false),
                    productSegments = table.Column<string>(type: "text", nullable: false),
                    productCatalog = table.Column<string>(type: "text", nullable: false),
                    hasGovOrder = table.Column<string>(type: "text", nullable: false),
                    capacityUtilization = table.Column<string>(type: "text", nullable: false),
                    hasExport = table.Column<string>(type: "text", nullable: false),
                    exportPrevYear = table.Column<int>(type: "integer", nullable: false),
                    exportCountries = table.Column<string>(type: "text", nullable: false),
                    legalCoords = table.Column<string>(type: "text", nullable: false),
                    productionCoords = table.Column<string>(type: "text", nullable: false),
                    additionalCoords = table.Column<string>(type: "text", nullable: false),
                    latitude = table.Column<int>(type: "integer", nullable: false),
                    longitude = table.Column<int>(type: "integer", nullable: false),
                    okrug = table.Column<string>(type: "text", nullable: false),
                    district = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Companies", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "AspNetRoleClaims",
                columns: table => new
                {
                    Id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    RoleId = table.Column<long>(type: "bigint", nullable: false),
                    ClaimType = table.Column<string>(type: "text", nullable: true),
                    ClaimValue = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetRoleClaims", x => x.Id);
                    table.ForeignKey(
                        name: "FK_AspNetRoleClaims_AspNetRoles_RoleId",
                        column: x => x.RoleId,
                        principalTable: "AspNetRoles",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "AspNetUserClaims",
                columns: table => new
                {
                    Id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    UserId = table.Column<long>(type: "bigint", nullable: false),
                    ClaimType = table.Column<string>(type: "text", nullable: true),
                    ClaimValue = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserClaims", x => x.Id);
                    table.ForeignKey(
                        name: "FK_AspNetUserClaims_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "AspNetUserLogins",
                columns: table => new
                {
                    LoginProvider = table.Column<string>(type: "text", nullable: false),
                    ProviderKey = table.Column<string>(type: "text", nullable: false),
                    ProviderDisplayName = table.Column<string>(type: "text", nullable: true),
                    UserId = table.Column<long>(type: "bigint", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserLogins", x => new { x.LoginProvider, x.ProviderKey });
                    table.ForeignKey(
                        name: "FK_AspNetUserLogins_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "AspNetUserRoles",
                columns: table => new
                {
                    UserId = table.Column<long>(type: "bigint", nullable: false),
                    RoleId = table.Column<long>(type: "bigint", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserRoles", x => new { x.UserId, x.RoleId });
                    table.ForeignKey(
                        name: "FK_AspNetUserRoles_AspNetRoles_RoleId",
                        column: x => x.RoleId,
                        principalTable: "AspNetRoles",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_AspNetUserRoles_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "AspNetUserTokens",
                columns: table => new
                {
                    UserId = table.Column<long>(type: "bigint", nullable: false),
                    LoginProvider = table.Column<string>(type: "text", nullable: false),
                    Name = table.Column<string>(type: "text", nullable: false),
                    Value = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserTokens", x => new { x.UserId, x.LoginProvider, x.Name });
                    table.ForeignKey(
                        name: "FK_AspNetUserTokens_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "TokenStorage",
                columns: table => new
                {
                    TokenId = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    UserId = table.Column<long>(type: "bigint", nullable: false),
                    RefreshToken = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_TokenStorage", x => x.TokenId);
                    table.ForeignKey(
                        name: "FK_TokenStorage_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_AspNetRoleClaims_RoleId",
                table: "AspNetRoleClaims",
                column: "RoleId");

            migrationBuilder.CreateIndex(
                name: "RoleNameIndex",
                table: "AspNetRoles",
                column: "NormalizedName",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUserClaims_UserId",
                table: "AspNetUserClaims",
                column: "UserId");

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUserLogins_UserId",
                table: "AspNetUserLogins",
                column: "UserId");

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUserRoles_RoleId",
                table: "AspNetUserRoles",
                column: "RoleId");

            migrationBuilder.CreateIndex(
                name: "EmailIndex",
                table: "AspNetUsers",
                column: "NormalizedEmail");

            migrationBuilder.CreateIndex(
                name: "UserNameIndex",
                table: "AspNetUsers",
                column: "NormalizedUserName",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_TokenStorage_UserId",
                table: "TokenStorage",
                column: "UserId",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "AspNetRoleClaims");

            migrationBuilder.DropTable(
                name: "AspNetUserClaims");

            migrationBuilder.DropTable(
                name: "AspNetUserLogins");

            migrationBuilder.DropTable(
                name: "AspNetUserRoles");

            migrationBuilder.DropTable(
                name: "AspNetUserTokens");

            migrationBuilder.DropTable(
                name: "Companies");

            migrationBuilder.DropTable(
                name: "TokenStorage");

            migrationBuilder.DropTable(
                name: "AspNetRoles");

            migrationBuilder.DropTable(
                name: "AspNetUsers");
        }
    }
}
